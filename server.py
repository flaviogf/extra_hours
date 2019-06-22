from datetime import datetime

from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.get('/')
def status(request):
    response = {'data': datetime.now().strftime('%Y-%m-%d %H:%M'), 'errors': []}
    return json(response, headers={'ip': request.ip})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
