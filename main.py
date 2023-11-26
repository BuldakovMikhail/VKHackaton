from nn_framework.WebServer import WebServer
from nn_framework.ReqParser import ReqParser
from nn_framework.render_template import render_template
from nn_framework.Response import Response

app = WebServer()

@app.add_handler('/')
def index_handler(session: ReqParser):
    resp = Response()
    resp.body = render_template('./main_page.html', {})
    return resp

@app.add_handler('/refresh')
def refresh_handler(session: ReqParser):
    n_amount = session.get_cookies().get('n_amount', 0)
    resp = Response()
    resp.body = render_template('./count_refresh.html', locals())
    resp.set_cookie('n_amount', int(n_amount) + 1, 60 * 60 * 24)
    return resp

@app.add_handler('/binding/<test>')
def binding_example(session: ReqParser):
    test = session.url.replace('/binding/', '')
    n_amount = session.get_cookies().get('n_amount', 0)
    resp = Response()
    resp.body = render_template('./binding_test.html', locals())
    return resp

app.run('0.0.0.0', 8080)