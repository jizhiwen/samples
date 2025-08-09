## 生成证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem -subj "/CN=a.codelines.top"

## 生成密码
docker run --rm jupyter:latest python3 -c "from jupyter_server.auth import passwd; print(passwd('123456'))"

## 运行容器
docker run -d --restart=unless-stopped  --name jupyter -v ${PWD}/samples:/samples -w /samples -p 8888:8888 jupyter:latest jupyter lab --allow-root --no-browser --ServerApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$l4oHXHXCvijbG/qB4rSYMg$vxBml7/kJ8eEC26gND2u2z8qQtuq/PzcKh6E0jGuiA0' --ServerApp.allow_remote_access=True --ip=0.0.0.0  --port=8888 --ServerApp.root_dir=/samples --certfile=/samples/cert.pem --keyfile=/samples/key.pem

## 进入容器设置环境
### 设置hf 镜像
cat <<EOF > ~/.bash_aliases
alias set-hf-mirror='export HF_ENDPOINT=https://hf-mirror.com'
EOF

### 安装 JupyterLab 插件
pip install ipywidgets jupyterlab-execute-time -i https://mirrors.ustc.edu.cn/pypi/simple
