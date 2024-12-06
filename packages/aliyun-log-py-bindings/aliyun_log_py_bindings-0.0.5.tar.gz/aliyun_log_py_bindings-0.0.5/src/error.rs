use prost::DecodeError;
use pyo3::exceptions::{PyUnicodeDecodeError, PyValueError};
use pyo3::PyErr;
use thiserror::Error;

#[derive(Debug, Error)]
pub(crate) enum AliyunLogError {
    #[error(transparent)]
    DecodeProtobuf(#[from] DecodeError),

    #[error(transparent)]
    DecodeUtf8Str(#[from] std::str::Utf8Error),

    #[error(transparent)]
    DecodeJson(#[from] serde_json::Error),
}

impl From<AliyunLogError> for PyErr {
    fn from(err: AliyunLogError) -> PyErr {
        match err {
            AliyunLogError::DecodeProtobuf(e) => PyErr::new::<PyValueError, _>(format!("{}", e)),
            AliyunLogError::DecodeUtf8Str(e) => {
                PyErr::new::<PyUnicodeDecodeError, _>(format!("{}", e))
            }
            AliyunLogError::DecodeJson(e) => PyErr::new::<PyValueError, _>(format!("{}", e)),
        }
    }
}
