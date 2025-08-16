#!/bin/sh
python3 -m venv .env_docs
source .env_docs/bin/activate
pip install --quiet sphinx myst_parser -i https://mirrors.ustc.edu.cn/pypi/simple
make html
