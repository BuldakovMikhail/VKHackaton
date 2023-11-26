# class CookieObj:
#     def __init__(self, value, expire_time):
#         self.value = value
#         self.expire_time = expire_time


class Response:
    def __init__(self) -> None:
        self.__body = ""  # Строка ответ хендлера
        self.__headers = []  # Заголовки созданные хендлером
        # self.__cookies = {}

    def __str__(self) -> str:
        response_str = "\r\n".join(self.__headers) + "\r\n\r\n" + self.__body
        return response_str

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

    # def append_cookie(self, key, cookie_data):
    #     self.__cookies[key] = cookie_data

    # def set_cookie()

    # @property
    # def cookies(self):
    #     return self.__cookies

    # @cookies.setter
    # def cookies(self, cookies):
    #     self.__cookies = cookies


if __name__ == "__main__":
    # cookies = CookieData(1, "time of expire")
    resp = Response()
    resp.body = "shreck"
    resp.headers = ["boloto Shrecka", "Pivo"]
    print(str(resp))
