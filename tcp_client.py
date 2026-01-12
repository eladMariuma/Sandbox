import socket

HOST = "127.0.0.1"
PORT = 8000

def recv_line(sock: socket.socket):
    buf = b""
    while '\n' not in buf:
        chunk =  sock.recv(1024)
        if not chunk:
            raise ConnectionError("Connection closed by remote host")
        buf += chunk
    line, rest = buf.split(b"\n", 1)
    return line.decode("utf8")

if __name__ == "__main__":
    with socket.create_connection((HOST, PORT), timeout=3) as sock:
        sock.sendall("Hello world".encode("utf8"))
        print(recv_line(sock))