import os
import socket
import struct

def recv_all(conn, length):
    """确保接收指定长度的数据"""
    data = b''
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data

# 创建socket对象 tcp
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.connect(('127.0.0.1', 8000))

print("客户端已连接到服务端")

while True:
    try:
        cmd = sk.recv(1024)
        if not cmd:
            print("服务端断开连接")
            break

        cmd_str = cmd.decode("utf-8").strip()
        print(f"收到命令: {cmd_str}")

        # ========== 处理 getfile: 上传文件给服务端 ==========
        if cmd_str.startswith("getfile "):
            file_path = cmd_str[8:].strip()
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    file_data = f.read()
                sk.send(struct.pack("i", len(file_data)))
                sk.sendall(file_data)
                print(f"✅ 已发送文件: {file_path}")
            else:
                error_msg = f"ERROR: 文件不存在 - {file_path}".encode("utf-8")
                # 发送负数表示错误消息
                sk.send(struct.pack("i", -len(error_msg)))
                sk.sendall(error_msg)

        # ========== 处理 putfile: 接收服务端上传的文件 ==========
        elif cmd_str.startswith("putfile "):
            parts = cmd_str.split(" ", 2)
            if len(parts) != 3:
                error_msg = "ERROR: putfile 格式错误".encode("utf-8")
                sk.send(struct.pack("i", len(error_msg)))
                sk.sendall(error_msg)
                continue

            _, local_file, remote_path = parts
            print(f"准备接收文件: {local_file} -> {remote_path}")

            # 接收文件大小
            size_data = recv_all(sk, 4)
            if not size_data:
                print("服务端断开")
                break
            file_size = struct.unpack("i", size_data)[0]

            # 如果文件大小为负数，表示服务端发送了错误消息
            if file_size < 0:
                error_data = recv_all(sk, abs(file_size))
                if error_data:
                    print("服务端错误:", error_data.decode("utf-8", errors="replace"))
                continue

            # 接收文件内容
            file_data = recv_all(sk, file_size)
            if not file_data:
                print("接收文件失败")
                break

            # 保存文件并发送响应给服务端
            try:
                os.makedirs(os.path.dirname(remote_path), exist_ok=True)
                with open(remote_path, "wb") as f:
                    f.write(file_data)
                success_msg = f"SUCCESS: 文件已保存 - {remote_path}".encode("utf-8")
                sk.send(struct.pack("i", len(success_msg)))
                sk.sendall(success_msg)
                print(f"✅ 文件已保存: {remote_path}")
            except Exception as e:
                error_msg = f"ERROR: 保存失败 - {str(e)}".encode("utf-8")
                sk.send(struct.pack("i", len(error_msg)))
                sk.sendall(error_msg)
                print(f"❌ 保存失败: {e}")

        # ========== 普通命令 ==========
        else:
            try:
                result = os.popen(cmd_str).read()
                data = result.encode("utf-8", errors="replace")
            except Exception as e:
                data = f"Command execution error: {str(e)}".encode("utf-8")

            data_size = len(data)
            sk.send(struct.pack("i", data_size))
            sk.sendall(data)

    except (ConnectionResetError, BrokenPipeError):
        print("服务端意外断开")
        break
    except Exception as e:
        print(f"客户端错误: {e}")
        break

sk.close()
