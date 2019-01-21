from flask import Flask, jsonify, request
from werkzeug.wrappers import Response
from Manager.ProxyManager import ProxyManager


app = Flask(__name__)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response,environ)


app.response_class = JsonResponse

api_list = {
    'get': u'get an usable proxy',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete an unable proxy',
    'get_status': u'proxy statistics'
}


@app.route('/')
def index():
    return api_list


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


@app.route('/refresh')
def refresh():
    return 'success'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    return proxies if proxies else 'no proxies'


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'delete success'


@app.route('/get_status/')
def getStatus():
    status = ProxyManager().getNumber()
    return status


def run():
    app.run(host='127.0.0.1', port=5010)


if __name__ == '__main__':
    run()
