# README

## constructor
- handler
    - 各种推理服务的源码
- model
    - 数据结构定义
- util
    - 工具类
- common
    - 全局变量
- app.py
    - 程序入口
- config.yaml
    - 配置文件    



## 踩坑记录
- 使用linux跑，而不是windows
```shell
docker run -d -it --gpus all -p 4000:4000 -v /root/data/sd_models/models:/sd_models -v /mnt/d/university/GraduationDesign/GraduationDesign/infer/:/app registry.cn-hangzhou.aliyuncs.com/stable_diffusion_origami/sd:infer_v1.1
```
**在windows，也就是这里修改代码，但是在wsl中docker中跑代码**



- minikube不能直接用hostPath进行mount，需要使用
```shell
minikube stop
minikube delete
minikube start --mount-string="/root/graduation_design:/mnt" --mount --force
eval $(minikube docker-env)
```

- minikube拉去img报错
```
minikube ssh进入容器
sudo apt-get update
sudo apt install vim
vim /etc/docker/daemon.json
# 添加以下信息
"registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
```

``
- k8s特别好用的一个测试命令
```shell
# 实现端口转发，可以转发pod, svc, etc.
kubectl port-forward --address 0.0.0.0 pod/infer-ss-0 8081:80
```

- k8s 代理
```shell
# 让外网也能访问
kc proxy --port=8080 --address=0.0.0.0 --accept-hosts='^*$'
```