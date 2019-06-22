FROM python:3.7
WORKDIR /app
RUN pip install pipenv==2018.11.26
COPY ./Pipfile ./Pipfile
RUN pipenv install
RUN pipenv install gunicorn==19.9.0
COPY . .
EXPOSE 80
CMD ["pipenv", "run", "gunicorn", "server:app", "--bind", "0.0.0.0:80", "--worker-class", "sanic.worker.GunicornWorker"]
