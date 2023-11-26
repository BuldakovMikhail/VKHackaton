from WebServer import HandlersContainer
import unittest


def test_f():
    return "a"


def test_f2():
    return "b"


class TestHandlersContainer(unittest.TestCase):
    def test_add_handler(self):
        container = HandlersContainer()
        st = "/dsa/fd/asd/fds"
        container.add_handler(st, test_f)

    def test_add_handler_with_template(self):
        container = HandlersContainer()
        st = "/dsa/<t>/asd/fds"
        container.add_handler(st, test_f)

    def test_add_handler_with_two_templates(self):
        container = HandlersContainer()
        st = "/dsa/<t>/asd/fds/<asd>"
        container.add_handler(st, test_f)

    def test_add_handler_and_get(self):
        container = HandlersContainer()
        st = "/dsa/asd/fds"
        container.add_handler(st, test_f)

        url = "/dsa/asd/fds"
        res = container.try_call_handler(url)

        self.assertIsNotNone(res)

    def test_add_handler_and_get_not_none(self):
        container = HandlersContainer()
        st = "/dsa/asd/fds"
        container.add_handler(st, test_f)

        url = "/dsa/asd"
        res = container.try_call_handler(url)

        self.assertIsNone(res)

    def test_add_handler_and_get_with_template(self):
        container = HandlersContainer()
        st = "/dsa/<t>/fds"
        container.add_handler(st, test_f)

        url = "/dsa/1/fds"
        res = container.try_call_handler(url)

        self.assertIsNotNone(res)
        self.assertEqual(res, test_f)

        url = "/dsa/2/fds"
        res = container.try_call_handler(url)

        self.assertIsNotNone(res)
        self.assertEqual(res, test_f)

    def test_add_handler_and_get_with_two_paths(self):
        container = HandlersContainer()
        st = "/a/d/b"
        container.add_handler(st, test_f)

        st = "/a/c"
        container.add_handler(st, test_f2)

        url = "/a/d/b"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f)

        url = "/a/d/b"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f)

        url = "/a/c"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f2)

    def test_add_two_handlers_templates(self):
        container = HandlersContainer()
        st1 = "/dsa/1/<t>"
        container.add_handler(st1, test_f)
        st2 = "/dsa/<t>"
        container.add_handler(st2, test_f2)

        url = "/dsa/1/fds"
        res = container.try_call_handler(url)

        self.assertIsNotNone(res)
        self.assertEqual(res, test_f)

        url = "/dsa/2"
        res = container.try_call_handler(url)

        self.assertIsNotNone(res)
        self.assertEqual(res, test_f2)

    def test_add_handler_and_get_with_two_paths_and_templ(self):
        container = HandlersContainer()
        st = "/a/<t>/b"
        container.add_handler(st, test_f)

        st = "/a/c"
        container.add_handler(st, test_f2)

        url = "/a/1/b"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f)

        url = "/a/2/b"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f)

        url = "/a/c"
        res = container.try_call_handler(url)
        self.assertEqual(res, test_f2)
