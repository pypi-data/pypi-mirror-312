## 介绍

这是一个使用 Maturin + PyO3 构建的库，用于加速 Aliyun SLS Python SDK。底层使用 Rust 语言编写，通过兼容 Python API，使得
Python 代码可以调用底层 Rust。

本仓库基于 pyo3 abi3-py37，支持 Python >= 3.7 的所有 Python
解释器，兼容性具体可参考文档[abi3](https://pyo3.rs/v0.23.2/features.html?highlight=abi3#abi3)。

Rust 代码会被编译成动态库，然后被 Maturin 打包成 wheel 文件。不同平台上可以构建适用于该平台的 wheel 构建产物，也可以交叉编译。

## 编译

安装 [maturin](https://github.com/PyO3/maturin) 与 [rust](https://www.rust-lang.org/learn/get-started)

```bash
pip install maturin
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

执行构建脚本

```bash
./build.sh
```

## 交叉编译

也支持交叉编译，建议用 zig 交叉编译

```bash
pip install ziglang
rustup target add x86_64-unknown-linux-gnu
maturin build --release --target x86_64-unknown-linux-gnu --zig
```

## 测试

```bash
source .venv/bin/activate
pip install .[dev]
./test/test.sh
```

## benchmark

```bash
export BENCHMARK_TEST_WORKDIR="your/workdir/path/with/dataset"
cargo bench
```

## API

支持的 API 可以参考[aliyun_log_py_bindings](aliyun_log_py_bindings)目录下的 pyi 文件

## 发布版本

打 tag，然后手动运行 Release Workflow，选择对应 tag。