#!/bin/bash
set -e

MODE=${1:---release}
echo "Build on mode MODE"

# 检查 Python 是否安装
command -v python >/dev/null 2>&1 || { echo "Python is not installed. Exiting." >&2; exit 1; }

# 检查并创建虚拟环境
if [ -d ".venv" ]; then
  echo 'Using existing virtual environment'
else
  echo 'Creating virtual environment'
  python -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate
# 清除 CONDA_PREFIX 环境变量
unset CONDA_PREFIX

maturin develop $MODE
maturin build $MODE