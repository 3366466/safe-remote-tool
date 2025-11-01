# safe-remote-tool
Educational remote admin tool: execute CMD commands, download files (getfile), upload files (putfile). For authorized security research only.教育远程管理工具：执行CMD命令，下载文件（getfile），上传文件（putfile）。仅供授权的安全研究使用。

这是一个基于 Python Socket 的远程管理工具，支持文件传输和命令执行功能。

## 功能特性

- **文件上传**：从服务端上传文件到客户端
- **文件下载**：从客户端下载文件到服务端  
- **命令执行**：在客户端执行系统命令
- **错误处理**：完善的错误处理和协议验证
- **跨平台**：支持 Windows、Linux、macOS

## 文件结构

```
trojan/   木马/
├── client2.py    # 客户端程序
├── server2.py    # 服务端程序
└── README.md     # 说明文档
```

## 安装要求

- Python 3.6+   - Python 3.6- Python 3.6 - Python 3.6
- 无需额外依赖库

## 使用方法

### 1. 启动服务端

```bash   ”“bash
python trojan/server2.py
```

服务端将在 `0.0.0.0:8000` 监听客户端连接。

### 2. 启动客户端

```bash   ”“bash
python trojan/client2.py
```

客户端将自动连接到 `127.0.0.1:8000`。

### 3. 可用命令

在服务端输入以下命令：

#### 文件操作命令

- **下载文件**：`getfile <客户端文件路径>`
  - 示例：`getfile test_file.txt`
  - 文件将保存到服务端的 `downloads/` 目录

- **上传文件**：`putfile <服务端文件路径> <客户端保存路径>`
  - 示例：`putfile test_file.txt uploaded.txt`
  - 将服务端文件上传到客户端指定位置

#### 系统命令

- **执行命令**：直接输入系统命令
  - 示例：`dir` (Windows) 或 `ls` (Linux/macOS)
  - 示例：`ipconfig` 或 `ifconfig`

#### 退出命令

- **退出连接**：`q`

## 协议说明

### 数据传输协议

- **文件传输**：发送正数大小 + 文件数据
- **错误消息**：发送负数大小 + 错误消息
- **响应确认**：客户端在保存文件后发送响应给服务端

### 错误处理

- 文件不存在时会返回明确的错误信息
- 网络断开连接时会自动重连
- 协议错误时会进行适当的清理和恢复

## 使用示例

### 基本操作流程

1. 启动服务端：
   ```bash   ”“bash   ”“bash”“bash“bash”“bash”“bash”“bash”“bash”“bash”“bash”“bash“bash”“bash”“bash”“bash”
   python trojan/server2.py   python木马/ server2.py
   ```

2. 启动客户端：
   ```bash   ”“bash   ”“bash”“bash“bash”“bash”“bash”“bash”
   python trojan/client2.py   python木马/ client2.py
   ```

3. 在服务端输入命令：
   ```
   等待客户端连接...
   [('127.0.0.1', 12345)] 已上线
   >> getfile test_file.txt
   ✅ 文件已下载: downloads/test_file.txt
   
   >> putfile test_file.txt client_test.txt
   ✅ 已发送文件 (123 bytes)
   客户端响应: SUCCESS: 文件已保存 - client_test.txt
   
   >> dir   > >目录
   结果: [目录列表内容]
   ```

## 注意事项

1. **安全性**：此工具仅用于学习和测试目的，请勿用于非法用途
2. **防火墙**：确保 8000 端口未被防火墙阻止
3. **文件权限**：确保有足够的文件读写权限- Python 3.6- Python 3.6- Python 3.6
4. **网络环境**：确保客户端和服务端在同一个网络或可互相访问

## 故障排除

### 常见问题

1. **连接失败**：
   -   python木马/ server2.py 检查服务端是否已启动
   - 检查防火墙设置
   - 确认端口 8000 未被占用
   ”“bash   ”“bash
2.   python木马/ server2.py   python木马/ server2.py **文件传输失败**：
   - 检查文件路径是否正确
   - 确认有足够的磁盘空间
   - 检查文件权限   ”“bash”“bash

3. **命令执行无响应**：
   - 检查客户端系统是否支持该命令
   - 确认命令语法正确   ”“bash”“bash

## 开发说明

### 代码结构

- `client2.py`：客户端主程序，处理命令接收和文件传输
- `server2.py`：服务端主程序，提供命令输入和文件管理

### 扩展功能

可以在此基础上添加以下功能：
- 加密通信
- 多客户端支持
- 图形界面
- 日志记录
- 配置文件支持

## 许可证

本项目仅用于学习和研究目的。
