FROM python:3.7
WORKDIR /app
RUN pip install pipenv
COPY ./Pipfile ./Pipfile
RUN pipenv install
COPY . .
CMD ["pipenv", "run", "python", "server.py"]
