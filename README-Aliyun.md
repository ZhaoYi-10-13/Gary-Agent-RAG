# 🚀 阿里云部署服务指南

**以下步骤展示如何在阿里云 ECS 上快速部署项目并开放公网访问。**

---

## 1. 购买与登录 ECS
1. 打开阿里云个人主页，点击 **立即体验**。  
2. 在顶部导航栏中选择 **产品** → **云服务器 ECS** → **立即购买**。  
3. 选择最低配置（最低仅需 **99 元 / 年**），也可以选择试用（但会有服务限制）。  
4. 下单完成后进入 **控制台**，点击 **远程连接**，即可自动进入 **Terminal 界面**。

---

## 2. 克隆项目与环境配置
在基础的ECS服务器中下载可能需要一段时间
```bash  
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.11 及其工具
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils

# 安装常用工具
sudo apt install -y git curl build-essential

# 克隆项目
git clone https://github.com/ShenSeanChen/yt-rag.git
cd yt-rag

# 创建虚拟环境
python3.11 -m venv venv_yt_rag
source venv_yt_rag/bin/activate 

# 安装依赖
pip install -r requirements.txt
```
剩下的步骤和文档里的一样，确保测试通过即可
⸻

## 3. 启动服务

使用以下命令之一启动服务（根据需要选择端口）：

```bash
uvicorn main:app --host 0.0.0.0 --port 80
# 或者
uvicorn main:app --host 0.0.0.0 --port 8000
```
	•	8000 端口：开发与调试推荐
	•	80 端口：生产环境推荐（无需加端口号）

⸻

## 4. 配置防火墙 (UFW)

检查并放行端口：

```bash
# 查看状态
sudo ufw status

# 开启 UFW（如果未启用）
sudo ufw enable

# 放行 SSH + HTTP/HTTPS + 开发端口
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp

# 重载规则
sudo ufw reload
```

⸻

## 5. 配置安全组

进入阿里云控制台 → ECS → 网络与安全组 → 安全组：
	1.	选择 添加入方向规则
	2.	协议类型选择：
	•	自定义 TCP（端口 8000）
	•	或者 Web HTTP 流量（端口 80）
	3.	访问来源：0.0.0.0/0（允许任何位置访问）
	4.	优先级和授权策略保持默认
	5.	点击 确定 保存

⸻

## 6. 检查服务运行状态

在云服务器终端运行：
```bash
# 如果跑在 8000 端口
curl http://127.0.0.1:8000/healthz

# 如果跑在 80 端口
curl http://127.0.0.1/healthz
```
正常输出示例：
```bash
{"status":"degraded","database_connected":false}
```
说明服务已启动成功（提示 degraded 是正常的，因为数据库服务器在国外）。

⸻

## 7. 浏览器访问
	1.	回到阿里云 控制台 → 网络与安全组
	2.	在左侧找到 公网 IP 并复制
	3.	在浏览器输入：

	•	如果是 8000 端口：

http://<公网IP>:8000/chat


	•	如果是 80 端口：

http://<公网IP>/chat


即可进入聊天页面 🎉




