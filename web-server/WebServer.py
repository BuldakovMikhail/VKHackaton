import socket


class Response:
    body = 'body'
    headers = ['header1', 'header2']
    status = 200
    
# /user/<uid>/afsaf/<aboba>
# /user/prikol
# url?key1=value1&key2=value2

# localhost:8081/user/228/1337
# localhost:8081/user/sheesh/1337

#/user/<uid>
#/user/<uid2>/<fff>
#/user/main



# uid=228, aboba=1337

class HandlersContainer:
    def add_handler(url, func): pass
    def try_call_handler(url) -> (bool, Response): pass

class WebServer:
    def __init__(self):
        self.m_handlers = {}

    def add_handler(self, url):
        if url in self.m_handlers:
            raise RuntimeError('Обработчик такой ссылки уже существует!')
        
        def wrapper(func):
            self.m_handlers[url] = func
            return func
        
        return wrapper

    def run(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

        while True:
            client_socket, client_address = self.server_socket.accept()
            
            request = client_socket.recv(1024).decode()
            request_lines = request.split('\r\n')
            method, path, version = request_lines[0].split()

            path, params = self.__parse_params(path)

            print(f'{client_address[0]} {method} {path} {version}')

            if path not in self.m_handlers:
                resp = Response()
                resp.body = 'error 404'
                resp.status = 404
                raw_response = self.__response_to_str(resp)
            else:
                raw_response = self.__response_to_str(self.m_handlers[path]())
            
            client_socket.sendall(raw_response.encode())

            client_socket.close()

    def __response_to_str(self, response: Response):
        response_headers = [
            f'HTTP/1.1 {response.status} OK',
            'Content-Type: text/html; charset=utf-8',
            f'Content-Length: {len(response.body)}',
            'Connection: close',
        ]
        response_raw = '\r\n'.join(response_headers) + '\r\n\r\n' + response.body
        return response_raw
    
    def __parse_params(self, path):
        url, params = path.split('?')
        params = params.split('&')
        params_dict = {}
        for parameter in params:
            key, val = parameter.split('=')
            params_dict[key]=val
        return url, params_dict


def render_template(html_name):
    with open(html_name, 'r') as file:
        resp = Response()
        resp.body = file.read()
        return resp


app = WebServer()


@app.add_handler('/user/<uid>/test/<another>')
def another_handler(uid, another):
    # request
    return render_template('web-server/main.html')

@app.add_handler('/message')
def test_handler():
   return render_template('web-server/message.html')

app.run('0.0.0.0', 8082)