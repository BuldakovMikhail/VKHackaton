import asyncio
import socket
# import urllib.parse
from ReqParser import ReqParser
from Response import Response

class WebServer:
    def __init__(self):
        self.m_handlers = {}

    def add_handler(self, url):
        if url in self.m_handlers:
            raise RuntimeError('Обработчик этого URL уже существует!')

        def wrapper(func):
            self.m_handlers[url] = func
            return func

        return wrapper

    async def handle_client(self, client_socket, client_address):
        loop = asyncio.get_event_loop()
        request = (await loop.sock_recv(client_socket, 1024)).decode()
        # request_lines = request.split('\r\n')
        # print(request)
        parsed_req = ReqParser(request)
        method, path, version = parsed_req.method, parsed_req.url, parsed_req.version
        # print(parsed_req.get_cookies())

        path, params = self.__parse_params(path)

        print(f'{client_address[0]} {method} {path} {version}')

        if path not in self.m_handlers:
            resp = Response()
            resp.body = 'error 404'
            resp.status = 404
            raw_response = self.__response_to_str(resp)
        else:
            raw_response = self.__response_to_str(self.m_handlers[path]())

        await loop.sock_sendall(client_socket, raw_response.encode())

        client_socket.close()

    async def run(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()

        loop = asyncio.get_event_loop()
        while True:
            client_socket, client_address = await loop.sock_accept(server_socket)
            await loop.create_task(self.handle_client(client_socket, client_address))

    def __response_to_str(self, response: Response):
        return response.export()

    def __parse_params(self, path):
        if '?' not in path:
            return path, {}
        url, params = path.split('?')
        params = params.split('&')
        params_dict = {}
        for parameter in params:
            key, val = parameter.split('=')
            params_dict[key]=val
        return url, params_dict


app = WebServer()

@app.add_handler('/user/<uid>/test/<another>')
def another_handler(uid, another):
    # request
    return render_template('web-server/main.html')

@app.add_handler('/message')
def test_handler():
    resp = render_template('web-server/message.html')
    resp.set_cookie('test', 'test_cookie', 100)
    return resp

def render_template(html_name):
    with open(html_name, 'r') as file:
        resp = Response()
        resp.body = file.read()
        return resp

async def main():
    await app.run('0.0.0.0', 8082)

asyncio.run(main())
