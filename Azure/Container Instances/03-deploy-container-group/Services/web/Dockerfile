FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["gunicorn", "-w", "4", "--chdir", "./app", "--bind", "0.0.0.0:80", "main:app"]