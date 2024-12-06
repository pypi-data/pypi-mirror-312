use aliyun_log_py_bindings::{json, log_parser, pb};
use criterion::{criterion_group, criterion_main, BatchSize, Criterion};
use lz4::block::decompress;
#[allow(unused)]
use prost::Message;
use pyo3::Python;
use serde_json::Value;
use std::path::PathBuf;
use std::{env, fs};

fn criterion_benchmark(c: &mut Criterion) {
    let workdir = PathBuf::from(
        env::var("BENCHMARK_TEST_WORKDIR")
            .expect("Environment variable BENCHMARK_TEST_WORKDIR is missing"),
    );
    let compressed_file = env::var("COMPRESSION_FILE").unwrap_or("compressed.data".to_string());
    let raw_data_file = env::var("RAW_DATA_FILE").unwrap_or("rawdata.data".to_string());
    let flat_json_file = env::var("FLAT_JSON_FILE").unwrap_or("flat.json".to_string());
    let compressed = fs::read(workdir.join(compressed_file)).expect("Cannot open compressed file");
    let raw_data = fs::read(workdir.join(raw_data_file)).expect("Cannot open raw data file");
    let raw_size = raw_data.len();
    #[allow(unused)]
    let flat_json_str =
        fs::read_to_string(workdir.join(flat_json_file)).expect("Cannot open flat json file");

    c.bench_function("raw data -> serde_json_node", |b| {
        b.iter(|| {
            serde_json::from_str::<Value>(&flat_json_str).unwrap();
        });
    });

    c.bench_function("lz4 decompress", |b| {
        b.iter(|| {
            decompress(compressed.as_slice(), Some(raw_size as i32)).unwrap();
        });
    });

    c.bench_function("pb -> serde_json_node", |b| {
        let log_group_list = pb::LogGroupListPb::decode(raw_data.as_slice()).unwrap();
        b.iter_batched(
            || log_group_list.clone(),
            |log_group_list| {
                log_parser::logs_to_flat_json_value(log_group_list);
            },
            BatchSize::LargeInput,
        );
    });

    {
        let mut group = c.benchmark_group("serde_json_node encode");
        group.bench_function("serde_json_node -> flat_json_py(utf8)", |b| {
            let value = serde_json::from_str::<Value>(&flat_json_str).unwrap();
            pyo3::prepare_freethreaded_python();
            b.iter_batched(
                || value.clone(),
                |value| {
                    Python::with_gil(|_py| json::load_value_recursively(_py, &value)).unwrap();
                },
                BatchSize::LargeInput,
            );
        });

        group.bench_function("serde_json_node -> str", |b| {
            let log_group_list = pb::LogGroupListPb::decode(raw_data.as_slice()).unwrap();
            b.iter_batched(
                || log_parser::logs_to_flat_json_value(log_group_list.clone()),
                |value| {
                    value.to_string();
                },
                BatchSize::LargeInput,
            );
        });
        group.finish();
    }

    {
        let mut group = c.benchmark_group("bytes_to_pb");
        group.bench_function("raw data -> pb", |b| {
            b.iter(|| {
                pb::LogGroupListPb::decode(raw_data.as_slice()).unwrap();
            });
        });
        group.bench_function("raw data -> pb(raw)", |b| {
            b.iter(|| {
                pb::LogGroupListRawPb::decode(raw_data.as_slice()).unwrap();
            });
        });
        group.finish();
    }
    {
        let mut group = c.benchmark_group("pb_to_py_flatten_json");
        group.bench_function("pb(raw) -> flat_json_py(utf8)", |b| {
            let log_group_list = pb::LogGroupListRawPb::decode(raw_data.as_slice()).unwrap();
            pyo3::prepare_freethreaded_python();
            b.iter_batched(
                || log_group_list.clone(),
                |log_group_list| {
                    Python::with_gil(|_py| {
                        log_parser::log_group_list_to_flat_json_py(_py, log_group_list, true, true)
                            .unwrap();
                    });
                },
                BatchSize::LargeInput,
            );
        });
        group.bench_function("pb(raw) -> flat_json_py(bytes)", |b| {
            let log_group_list = pb::LogGroupListRawPb::decode(raw_data.as_slice()).unwrap();
            pyo3::prepare_freethreaded_python();
            b.iter_batched(
                || log_group_list.clone(),
                |log_group_list| {
                    Python::with_gil(|_py| {
                        log_parser::log_group_list_to_flat_json_py(
                            _py,
                            log_group_list,
                            true,
                            false,
                        )
                        .unwrap();
                    });
                },
                BatchSize::LargeInput,
            );
        });
        group.finish();
    }
    {
        let mut group = c.benchmark_group("py api");
        group.bench_function("log_parser.logs_to_flat_json_str", |b| {
            pyo3::prepare_freethreaded_python();
            b.iter(|| {
                Python::with_gil(|_py| {
                    log_parser::logs_to_flat_json_str(_py, raw_data.as_slice()).unwrap();
                });
            });
        });
        group.bench_function("log_parser.lz4_logs_to_flat_json(utf8=true)", |b| {
            pyo3::prepare_freethreaded_python();
            b.iter(|| {
                Python::with_gil(|_py| {
                    log_parser::lz4_logs_to_flat_json(
                        _py,
                        compressed.as_slice(),
                        raw_size,
                        false,
                        true,
                    )
                    .unwrap();
                });
            });
        });
        group.bench_function("log_parser.lz4_logs_to_flat_json(utf8=false)", |b| {
            pyo3::prepare_freethreaded_python();
            b.iter(|| {
                Python::with_gil(|_py| {
                    log_parser::lz4_logs_to_flat_json(
                        _py,
                        compressed.as_slice(),
                        raw_size,
                        false,
                        false,
                    )
                    .unwrap();
                });
            });
        });
        group.bench_function("log_parser.lz4_logs_to_flat_json_str", |b| {
            pyo3::prepare_freethreaded_python();
            b.iter(|| {
                Python::with_gil(|_py| {
                    log_parser::lz4_logs_to_flat_json_str(_py, compressed.as_slice(), raw_size)
                        .unwrap();
                });
            });
        });
        group.bench_function("json.loads", |b| {
            pyo3::prepare_freethreaded_python();
            b.iter(|| {
                Python::with_gil(|_py| {
                    json::loads(_py, &flat_json_str).unwrap();
                });
            });
        });

        group.finish();
    }
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
