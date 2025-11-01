import socket
import struct
import os

# 创建socket对象tcp
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(("0.0.0.0", 8000))
sk.listen()

def recv(conn, total_size):
    """接收指定长度数据"""
    recv_size = 0
    recv_msg = b""
    while recv_size < total_size:
        recv_buffer = 1024 if (total_size - recv_size) > 1024 else (total_size - recv_size)
        data = conn.recv(recv_buffer)
        if not data:
            return None
        recv_msg += data
        recv_size += len(data)
    return recv_msg

def handle_putfile(conn, cmd):
    """服务端上传文件到客户端"""
    parts = cmd.split(b" ", 2)
    if len(parts) < 3:
        error_msg = "ERROR: putfile 格式: putfile 本地文件 远程路径".encode()
        # 发送负数表示错误消息
        conn.send(struct.pack("i", -len(error_msg)))
        conn.sendall(error_msg)
        return

    _, local_file, remote_path = parts
    local_file = local_file.decode("utf-8").strip()
    remote_path = remote_path.decode("utf-8").strip()

    print(f"准备上传文件: {local_file} → {remote_path}")

    # 检查服务端本地文件是否存在
    if not os.path.exists(local_file) or not os.path.isfile(local_file):
        error_msg = f"ERROR: 服务端本地文件不存在: {local_file}".encode("utf-8")
        # 发送负数表示错误消息
        conn.send(struct.pack("i", -len(error_msg)))
        conn.sendall(error_msg)
        print(f"❌ 文件不存在: {local_file}")
        return

    # 读取文件并发送
    try:
        with open(local_file, "rb") as f:
            file_data = f.read()
        file_size = len(file_data)
        conn.send(struct.pack("i", file_size))      # 发送正数文件大小
        conn.sendall(file_data)                     # 发送文件内容
        print(f"✅ 已发送文件 ({file_size} bytes)")
    except Exception as e:
        error_msg = f"ERROR: 读取文件失败 - {str(e)}".encode("utf-8")
        # 发送负数表示错误消息
        conn.send(struct.pack("i", -len(error_msg)))
        conn.sendall(error_msg)
        return

    # 等待客户端的响应（成功/失败）
    try:
        resp_size_data = recv(conn, 4)
        if resp_size_data:
            resp_size = struct.unpack("i", resp_size_data)[0]
            if resp_size > 0:
                resp_data = recv(conn, resp_size)
                if resp_data:
                    print("客户端响应:", resp_data.decode("utf-8", errors="replace"))
    except Exception as e:
        print("等待客户端响应时出错:", e)

        
while True:
    print("等待客户端连接...")
    try:
        conn, addr = sk.accept()
        print(f"[{addr}] 已上线")

        while True:
            try:
                cmd = input(">> ").encode("utf-8")
                if cmd == b"q":
                    conn.close()
                    break
                if not cmd:
                    continue

                conn.send(cmd)
                cmd_str = cmd.decode("utf-8").strip()

                # ========== 处理 getfile: 下载客户端文件 ==========
                if cmd_str.startswith("getfile "):
                    size_data = recv(conn, 4)
                    if not size_data:
                        print("客户端断开")
                        break
                    file_size = struct.unpack("i", size_data)[0]
                    
                    if file_size < 0:
                        error_data = recv(conn, abs(file_size))
                        if error_data:
                            print("客户端错误:", error_data.decode("utf-8", errors="replace"))
                        continue

                    file_data = recv(conn, file_size)
                    if not file_data:
                        print("接收文件时断开")
                        break

                    remote_path = cmd_str[8:].strip()
                    filename = os.path.basename(remote_path)
                    os.makedirs("downloads", exist_ok=True)
                    save_path = os.path.join("downloads", filename)
                    with open(save_path, "wb") as f:
                        f.write(file_data)
                    print(f"✅ 文件已下载: {save_path}")

                # ========== 处理 putfile: 上传文件到客户端 ==========
                elif cmd_str.startswith("putfile "):
                    handle_putfile(conn, cmd)

                # ========== 普通命令 ==========
                else:
                    size_data = recv(conn, 4)
                    if not size_data:
                        print("客户端断开")
                        break
                    total_size = struct.unpack("i", size_data)[0]
                    result = recv(conn, total_size)
                    if result is None:
                        break
                    print("结果:", result.decode("utf-8", errors="replace"))

            except (ConnectionResetError, BrokenPipeError):
                print(f"[{addr}] 客户端意外断开")
                break
            except Exception as e:
                print(f"处理命令出错: {e}")
                break

    except Exception as e:
        print(f"服务器错误: {e}")
