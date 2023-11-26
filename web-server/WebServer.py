import socket


class Response:
    body = "body"
    headers = ["header1", "header2"]
    status = 200


# /user/<uid>/afsaf/<aboba>
# /user/prikol
# url?key1=value1&key2=value2

# localhost:8081/user/228/1337
# localhost:8081/user/sheesh/1337

# /user/<uid> -> # /user/~
# /user/<uid2>/<fff> -> # /user/#/#
# /user/main

# uid=228, aboba=1337

# /user/<uid>
# /user/16

# /user/2/


# /user/<uid>/test/<another>-> kwargs == uid : 1, test: 2,
# uid=2 ,anither = 3
def find_in_list(l, val):
    for i, l_val in enumerate(l):
        if l_val == val:
            return i
    return None


class ANode:
    """
    Реализация узла произвольного дерева
    """

    def __init__(self, val=None, handler=None) -> None:
        self.childs = []
        self.val = val
        self.handler = handler


class AnyNode(ANode):
    def __init__(self):
        super().__init__()


class HandlersContainer:
    def __init__(self):
        self.root = ANode("/")  # root is always empty

    def __insert_seq(self, seq: list[str], handler):  # [abs,bds,<asd>]
        seq_id = 0
        cur_node = self.root

        while seq_id < len(seq):
            is_template = False
            if seq[seq_id].endswith(">") and seq[seq_id].startswith("<"):
                is_template = True

            cur_node_childs_vals = [child.val for child in cur_node.childs]
            
            if seq[seq_id] in cur_node_childs_vals:
                child_ind = cur_node_childs_vals.index(seq[seq_id])
                cur_node = cur_node.childs[child_ind]
            elif len(cur_node.childs) > 0 and isinstance(cur_node.childs[-1], AnyNode) and is_template:
                cur_node = cur_node.childs[-1]
            else:
                if is_template:
                    if (
                        len(cur_node.childs) > 0
                        and not isinstance(cur_node.childs[-1], AnyNode)
                    ) or len(cur_node.childs) == 0:
                        any_node = AnyNode()
                        if seq_id == len(seq) - 1:
                            any_node.handler = handler

                        cur_node.childs.append(any_node)
                        cur_node = cur_node.childs[-1]

                else:
                    val_node = ANode()
                    if seq_id == len(seq) - 1:
                        val_node.handler = handler
                    val_node.val = seq[seq_id]
                    cur_node.childs.insert(0, val_node)
                    cur_node = cur_node.childs[0]

            seq_id += 1

    def __get_handler(self, seq: list[str]):
        seq_id = 0
        cur_node = self.root

        while cur_node.childs and seq_id < len(seq):
            childs_vals = [c.val for c in cur_node.childs]

            if seq[seq_id] in childs_vals:
                child_ind = childs_vals.index(seq[seq_id])
                cur_node = cur_node.childs[child_ind]
                seq_id += 1
            elif isinstance(cur_node.childs[-1], AnyNode):
                cur_node = cur_node.childs[-1]
                seq_id += 1
            else:
                return None

        return cur_node.handler

    def __contains__(self, key: str) -> bool:
        handler = self.__get_handler(key.split("/")[1:])
        return handler is not None

    def add_handler(self, url, func):
        self.__insert_seq(url.split("/")[1:], func)

    def try_call_handler(self, url) -> (bool, Response):
        return self.__get_handler(url.split("/")[1:])


class WebServer:
    def __init__(self):
        self.m_handlers = {}

    def add_handler(self, url):
        if url in self.m_handlers:
            raise RuntimeError("Обработчик такой ссылки уже существует!")

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
            request_lines = request.split("\r\n")
            method, path, version = request_lines[0].split()

            path, params = self.__parse_params(path)

            print(f"{client_address[0]} {method} {path} {version}")

            if path not in self.m_handlers:
                resp = Response()
                resp.body = "error 404"
                resp.status = 404
                raw_response = self.__response_to_str(resp)
            else:
                raw_response = self.__response_to_str(self.m_handlers[path]())

            client_socket.sendall(raw_response.encode())

            client_socket.close()

    def __response_to_str(self, response: Response):
        response_headers = [
            f"HTTP/1.1 {response.status} OK",
            "Content-Type: text/html; charset=utf-8",
            f"Content-Length: {len(response.body)}",
            "Connection: close",
        ]
        response_raw = "\r\n".join(response_headers) + "\r\n\r\n" + response.body
        return response_raw

    def __parse_params(self, path):
        url, params = path.split("?")
        params = params.split("&")
        params_dict = {}
        for parameter in params:
            key, val = parameter.split("=")
            params_dict[key] = val
        return url, params_dict


def render_template(html_name):
    with open(html_name, "r") as file:
        resp = Response()
        resp.body = file.read()
        return resp


app = WebServer()


@app.add_handler("/user/<uid>/test/<another>")
def another_handler(uid, another):
    # request
    return render_template("web-server/main.html")


@app.add_handler("/message")
def test_handler():
    return render_template("web-server/message.html")


# app.run("0.0.0.0", 8082)
# container = HandlersContainer
# HandlersContainer =


def test_f():
    return "a"


def test_f2():
    return "b"


container = HandlersContainer()
st = "/a/<t>/b"
container.add_handler(st, test_f)

st = "/a/c"
container.add_handler(st, test_f2)

url = "/a/1/b"
res = container.try_call_handler(url)
# self.assertEqual(res, test_f)

url = "/a/2/b"
res = container.try_call_handler(url)
# self.assertEqual(res, test_f)

url = "/a/c"
res = container.try_call_handler(url)
# self.assertEqual(res, test_f2)
