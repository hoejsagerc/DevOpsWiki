FROM python:3.9.15-slim-buster as builder

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /usr/workdir

WORKDIR /usr/workdir

RUN python -m venv /usr/workdir/venv

ENV PATH="/usr/workdir/venv/bin:$PATH"

COPY --chown=python:python ./requirements.txt .

RUN pip install --no-cache -r requirements.txt

FROM python:3.9.15-slim-buster as production

RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y

RUN echo "[FreeTDS]\n\
Description = FreeTDS Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /usr/workdir && chown python:python /usr/workdir

WORKDIR /usr/workdir

COPY --chown=python:python --from=builder /usr/workdir/venv ./venv

COPY --chown=python:python . /usr/workdir/

WORKDIR /usr/workdir/app

USER 999

ENV PATH="/usr/workdir/venv/bin:$PATH"

RUN pip install pyodbc

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]