# conda create -n transformers python==3.10 ipykernel
# conda activate transformers
# python -m ipykernel install --user --name transformers
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -U transformers datasets evaluate accelerate timm -i https://mirrors.ustc.edu.cn/pypi/simple
pip install qwen_vl_utils -i https://mirrors.ustc.edu.cn/pypi/simple

HF_ENDPOINT=https://hf-mirror.com python -c "from transformers import pipeline; print(pipeline('sentiment-analysis')('hugging face is the best'))"
