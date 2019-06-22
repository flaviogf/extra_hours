from datetime import datetime

from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.get('/')
def status(request):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return json(body={'data': data, 'errors': []}, headers={'ip': request.ip})
