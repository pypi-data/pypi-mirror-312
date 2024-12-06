use crate::error::AliyunLogError;
use crate::pb;
use lz4::block::decompress;
use prost::Message;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyString};
use pyo3::{pyfunction, Bound, IntoPyObject, PyObject, PyResult, Python};
use serde_json::{Map, Value};

#[pyfunction]
pub fn logs_to_flat_json_str(py: Python, bytes: &[u8]) -> PyResult<String> {
    py.allow_threads(|| {
        let log_group_list = pb::LogGroupListPb::decode(bytes).map_err(AliyunLogError::from)?;
        Ok(pb_to_flat_json_str(log_group_list))
    })
}

#[pyfunction]
pub fn lz4_logs_to_flat_json_str(
    py: Python,
    compressed: &[u8],
    raw_size: usize,
) -> PyResult<String> {
    py.allow_threads(|| {
        let bytes = decompress(compressed, Some(raw_size as i32)).unwrap();
        let log_group_list =
            pb::LogGroupListPb::decode(bytes.as_slice()).map_err(AliyunLogError::from)?;
        Ok(pb_to_flat_json_str(log_group_list))
    })
}

#[pyfunction]
pub fn lz4_logs_to_flat_json(
    py: Python,
    bytes: &[u8],
    raw_size: usize,
    time_as_str: bool,
    decode_utf8: bool,
) -> PyResult<PyObject> {
    let log_group_list = py
        .allow_threads(|| {
            let decompressed = decompress(bytes, Some(raw_size as i32)).unwrap();
            pb::LogGroupListRawPb::decode(decompressed.as_slice())
        })
        .map_err(AliyunLogError::from)?;
    log_group_list_to_flat_json_py(py, log_group_list, time_as_str, decode_utf8)
}

pub fn logs_to_flat_json_value(log_group_list: pb::LogGroupListPb) -> Value {
    let mut logs = Vec::with_capacity(log_group_list.log_groups.len());
    for log_group in log_group_list.log_groups {
        let tag_kvs: Vec<(String, &str)> = log_group
            .log_tags
            .iter()
            .map(|log_tag| {
                let key = format!("__tag__:{}", log_tag.key);
                (key, log_tag.value.as_str())
            })
            .collect();
        let topic = log_group.topic.as_deref();
        let source = log_group.source.as_deref();
        for log in log_group.logs {
            let mut m = Map::with_capacity(4 + tag_kvs.len() + log.contents.len());
            for content in log.contents {
                m.insert(content.key, Value::from(content.value));
            }
            m.insert("__time__".to_string(), Value::from(log.time));
            if let Some(t) = topic {
                m.insert("__topic__".to_string(), Value::from(t));
            }
            if let Some(s) = source {
                m.insert("__source__".to_string(), Value::from(s));
            }
            if let Some(ns) = log.time_ns {
                m.insert("__time_ns__".to_string(), Value::from(ns));
            }
            for (k, v) in &tag_kvs {
                m.insert(k.clone(), Value::from(*v));
            }
            logs.push(Value::Object(m));
        }
    }
    Value::Array(logs)
}
fn pb_to_flat_json_str(log_group_list: pb::LogGroupListPb) -> String {
    logs_to_flat_json_value(log_group_list).to_string()
}

pub fn log_group_list_to_flat_json_py(
    py: Python,
    log_group_list: pb::LogGroupListRawPb,
    time_as_str: bool,
    decode_utf8: bool,
) -> PyResult<PyObject> {
    fn to_py_dict_vec(
        py: Python,
        log_group_list: pb::LogGroupListRawPb,
        time_as_str: bool,
        decode_utf8: bool,
    ) -> PyResult<Vec<Bound<PyDict>>> {
        let mut vec = Vec::with_capacity(log_group_list.log_groups.len());
        for log_group in log_group_list.log_groups {
            let tag_kvs: Vec<(String, &String)> = log_group
                .log_tags
                .iter()
                .map(|log_tag| {
                    let key = format!("__tag__:{}", log_tag.key);
                    (key, &log_tag.value)
                })
                .collect();
            let topic = log_group.topic.as_deref();
            let source = log_group.source.as_deref();
            let py_dict = PyDict::new(py);
            for log in log_group.logs {
                py_dict.set_item("__time__", get_time_py_object(py, log.time, time_as_str)?)?;
                if let Some(ns) = log.time_ns {
                    py_dict.set_item("__time_ns__", get_time_py_object(py, ns, time_as_str)?)?;
                }
                for content in log.contents {
                    set_py_dict(&py_dict, &content.key, &content.value, decode_utf8)?;
                }
                if let Some(t) = topic {
                    py_dict.set_item("__topic__", t)?;
                }
                if let Some(s) = source {
                    py_dict.set_item("__source__", s)?;
                }
                for (k, v) in &tag_kvs {
                    py_dict.set_item(k.as_str(), v.as_str())?;
                }
            }
            vec.push(py_dict);
        }
        Ok(vec)
    }
    let vec = to_py_dict_vec(py, log_group_list, time_as_str, decode_utf8)?;
    Ok(PyList::new(py, vec)?.into())
}

#[inline]
fn get_time_py_object(py: Python, value: u32, time_as_str: bool) -> PyResult<PyObject> {
    if time_as_str {
        Ok(PyString::new(py, &value.to_string()).into_any().into())
    } else {
        Ok(value.into_pyobject(py)?.into_any().into())
    }
}

#[inline]
fn set_py_dict(
    py_dict: &Bound<PyDict>,
    key: &str,
    value: &bytes::Bytes,
    decode_utf8: bool,
) -> PyResult<()> {
    if decode_utf8 {
        py_dict.set_item(key, std::str::from_utf8(value.as_ref())?)?;
    } else {
        py_dict.set_item(key, value.as_ref())?;
    }
    Ok(())
}
