FROM python:3.10.10-slim-buster

WORKDIR /app

COPY dist/toudou-*-py3-none-any.whl /app/
RUN pip install *.whl gunicorn

CMD ["gunicorn", "toudou.wsgi"]