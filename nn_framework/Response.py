class Response:
    def __init__(self) -> None:
        self.__status = 200
        self.__body = ""  # Строка ответ хендлера
        self.__headers = []  # Заголовки созданные хендлером

    def __str__(self) -> str:
        response_str = "\r\n".join(self.__headers) + "\r\n\r\n" + self.__body
        return response_str
    
    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str) -> None:
        self.__status = status

    @property
    def body(self) -> str:
        return self.__body

    @body.setter
    def body(self, body: str) -> None:
        self.__body = body

    @property
    def headers(self) -> list[str]:
        return self.__headers

    @headers.setter
    def headers(self, headers: list[str]) -> None:
        self.__headers = headers

    def append_header(self, header: str) -> None:
        self.__headers.append(header)

    def set_cookie(self, key, val, exp):
        self.append_header(f"Set-Cookie: {key}={val}; Max-Age={exp}")

    def export(self):
        response_headers = [
            f'HTTP/1.1 {self.status} OK',
            'Content-Type: text/html',
            'Connection: close',
        ] + self.__headers
        return '\r\n'.join(response_headers) + '\r\n\r\n' + self.body


if __name__ == "__main__":
    resp = Response()
    resp.body = "shreck"
    resp.headers = ["boloto Shrecka", "Pivo"]
    print(str(resp))
