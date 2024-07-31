import sys;
import os;
import socket;
from .constants import *

def MIME_map(ext):
    match ext:
        case TXT:
            return TEXT_PLAIN
        case HTML:
            return TEXT_HTML


def hd_header(socket):
    buffer = b''
    headers = []

    while True:
        chunk = socket.recv(1)

        if not chunk:
            break

        buffer += chunk

        if buffer.endswith(CRLF):
            to_append = buffer[:-len(CRLF)]

            headers.append(to_append)

            if to_append == b'': 
                break

            buffer = b''

    return headers

def hd_body(socket, buffer_size = BUFFER_SIZE):
    buffer = b''

    while len(buffer) < buffer_size:
        chunk = socket.recv(buffer_size - len(buffer))

        if not chunk:
            break

        buffer += chunk

        if BRANK_LINE in buffer:
            break

    return buffer

def parse_headers(headers):
    map_headers = {}
    headers = [header.decode(ENCODING).split(": ", 1) for header in headers]
    http = headers[0][0].split(" ")

    map_headers["Method"]=http[0]
    map_headers["Path"]=http[1]
    map_headers["Http-Bunner"]=http[2]

    for [header, value] in headers[1:-1]:
        map_headers[header] = value
    return map_headers

def handler(socket):
    headers = hd_header(socket)
    headers = parse_headers(headers)

    content_len = int(headers['Content-Length']) if 'Content-Length' in headers else BUFFER_SIZE
    body = hd_body(socket, content_len)

    return  resp_handler(socket, headers, body)

def resp_handler(socket, headers, body):
    content_type = headers['Content-Type'] if 'Content-Type' in headers else TEXT_PLAIN
    request_path = headers['Path'] if 'Path' in headers else SOURCE_PATH

    resp_stream = file_handler(content_type, request_path)

    socket.send("Today is Friday in California\r\n".encode(ENCODING))
    socket.close()

def file_handler(content_type, request_path):
    path = os.path.abspath(SOURCE_PATH)
    file = os.path.split(request_path)[-1]
    _, file_ext = os.path.splitext(file)

    mime_type = MIME_map(file_ext)
    
    absolute_file_path = "%s/%s".format(path,file)

    pass

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
            handler(socket)
    


if __name__ == "__main__":
    server = Server()

    if len(sys.argv) <= 1:
        server.listen()
    else: 
        server.listen(int(sys.argv[1]))
