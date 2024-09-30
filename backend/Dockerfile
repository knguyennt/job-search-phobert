FROM python:3.11.10-alpine

WORKDIR /app
COPY . .

RUN pip install poetry

RUN poetry install

CMD [ "poetry", "run", "flask", "run", "--host", "0.0.0.0" ]