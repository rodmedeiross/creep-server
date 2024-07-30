import sys;
import socket;

BUFFER_SIZE=1024
ENCODING="UTF-8"

class Server:
    def __init__(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        pass

    def listen(self, port = 8080):
        self._socket.bind(("0.0.0.0", port))
        self._socket.listen()

        print(f"Server listen in {port} port!")

        while True:
            socket, address =self._socket.accept()
            print(f"Socket created from {address}")
            self.handler(socket)
    
    def handler(self, socket):
        
        headers = self.parse_headers(self.hd_header(socket))

        if 'Content-Length' in headers:
            content_len = headers['Content-Length']
            content_len = int(content_len)
            body = self.hd_body(socket, content_len)
            print(body.decode(ENCODING))


        socket.send("Today is Friday in California\r\n".encode(ENCODING))
        return socket.close()

    def hd_header(self, socket):
        buffer = b''
        crlf = b'\r\n'
        crlf_len = len(crlf)

        headers = []

        while True:
            chunk = socket.recv(1)

            if not chunk:
                break

            buffer += chunk

            if buffer.endswith(crlf):
                to_append = buffer[:-crlf_len]
                headers.append(to_append)
                if to_append == b'': 
                    break
                buffer = b''

        return headers

    def hd_body(self, socket, buffer_size = BUFFER_SIZE):
        buffer = b''
        brank_line = b'\r\n\r\n'

        while len(buffer) < buffer_size:
            chunk = socket.recv(buffer_size - len(buffer))

            if not chunk:
                break

            buffer += chunk

            if brank_line in buffer:
                break

        return buffer

    def parse_headers(self, headers):
        hashmap_headers = {}
        headers = [header.decode(ENCODING).split(": ", 1) for header in headers][1:-1]
        for [header, value] in headers:
            hashmap_headers[header] = value
        return hashmap_headers

if __name__ == "__main__":
    server = Server()

    if len(sys.argv) <= 1:
        server.listen()
    else: 
        server.listen(int(sys.argv[1]))
