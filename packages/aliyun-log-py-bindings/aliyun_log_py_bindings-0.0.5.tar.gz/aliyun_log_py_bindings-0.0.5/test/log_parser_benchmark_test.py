import os
import threading

from aliyun_log_py_bindings import log_parser

workdir = os.getenv("BENCHMARK_TEST_WORKDIR")

with open(os.path.join(workdir, 'compressed.data'), 'rb') as f:
    compressed = f.read()

with open(os.path.join(workdir, 'rawdata.data'), 'rb') as f:
    rawdata = f.read()

raw_size = len(rawdata)
with open(os.path.join(workdir, 'flat.json'), 'r') as f:
    json_str = f.read()


def test_lz4_logs_to_flat_json_utf8(benchmark):
    benchmark(log_parser.lz4_logs_to_flat_json, compressed, raw_size, False, True)


def test_lz4_logs_to_flat_json_b_value(benchmark):
    benchmark(log_parser.lz4_logs_to_flat_json, compressed, raw_size, False, False)


def test_logs_to_flat_json_str(benchmark):
    benchmark(log_parser.logs_to_flat_json_str, rawdata)


def test_lz4_logs_to_flat_json_str(benchmark):
    benchmark(log_parser.lz4_logs_to_flat_json_str, compressed, raw_size)


def multi_threaded_task(num_threads, func, *args):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def test_lz4_logs_to_flat_json_n_threads():
    multi_threaded_task(4, log_parser.lz4_logs_to_flat_json, compressed, raw_size, False, True)
