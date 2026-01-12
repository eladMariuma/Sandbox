import logging
import socket
import threading
from typing import Optional, Callable

Handler = Callable[[str], str]

class TcpLinkServer:
    def __init__(
        self,
        host = '127.0.0.1',
        port = 8000,
        handler : Optional[Handler] = None
    ):
        self.host = host
        self.port = port
        self.handler = handler

        self._stop = threading.Event()
        self._thread : Optional[threading.Thread] = None
        self._sock : Optional[socket.socket] = None

    def start(self):
        if self._thread is not None:
            raise RuntimeError('Server is already running')

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # setsockopt(level, option_name, value)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((self.host, self.port))
        srv.listen(128)
        srv.settimeout(0.2)

        self._sock = srv
        self.port = srv.getsockname()[1]

        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
        self._sock = None

    def _serve(self):
        assert self._sock is None
        while not self._stop.is_set():
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break # Socket was closed
            threading.Thread(
                target=self._handle_client, args=(conn, addr), daemon=True
            ).start()

    def _handle_client(self, conn: socket.socket, addr):
        buf = b''

        with conn:
            while not self._stop.is_set():
                try:
                    chunk = conn.recv(1024)
                except OSError:
                    break
                if not chunk:
                    break

                buf += chunk

                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)

                    try:
                        msg = line.decode("utf-8")
                    except UnicodeDecodeError:
                        conn.sendall(b'ERR invalid utf-8\n')
                        continue

                    resp = self.handler(msg)
                    conn.sendall((resp + "\n").encode("utf-8"))

if __name__ == '__main__':
    server = TcpLinkServer('127.0.0.1', 8000)
    server.start()
    logging.info(f'Server started on port {server.host} {server.port}')
    logging.info('Press Ctrl+C to stop')
    try:
        while True:
            threading.Event().wait(1.0)
    except KeyboardInterrupt:
        logging.info('Stopping server')
    finally:
        server.stop()