use crate::error::AliyunLogError;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyList, PyString};
use pyo3::{pyfunction, IntoPyObject, Py, PyErr, PyObject, PyResult, Python};
use serde_json::Value;

#[pyfunction]
pub fn loads(py: Python, json_str: &str) -> PyResult<PyObject> {
    let value: Value = py
        .allow_threads(|| serde_json::from_str(json_str))
        .map_err(AliyunLogError::from)?;
    load_value_recursively(py, &value)
}

pub fn load_value_recursively(py: Python, value: &Value) -> PyResult<PyObject> {
    match value {
        Value::Null => Ok(py.None()),
        Value::Bool(b) => Ok(PyBool::new(py, *b).to_owned().into_any().into()),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(i.into_pyobject(py)?.into_any().into())
            } else if let Some(u) = n.as_u64() {
                Ok(u.into_pyobject(py)?.into_any().into())
            } else if let Some(f) = n.as_f64() {
                Ok(f.into_pyobject(py)?.into_any().into())
            } else {
                Err(PyErr::new::<PyValueError, _>(format!(
                    "Unsupported number type: {}",
                    n
                )))
            }
        }
        Value::String(s) => Ok(PyString::new(py, s).into()),
        Value::Array(arr) => {
            let py_list = PyList::empty(py);
            for item in arr {
                let py_item = load_value_recursively(py, item)?;
                py_list.append(py_item)?;
            }
            Ok(py_list.into())
        }
        Value::Object(obj) => {
            let py_dict = PyDict::new(py);
            for (key, value) in obj {
                let py_key: Py<PyString> = key.into_pyobject(py)?.into();
                let py_value = load_value_recursively(py, value)?;
                py_dict.set_item(py_key, py_value)?;
            }
            Ok(py_dict.into())
        }
    }
}
