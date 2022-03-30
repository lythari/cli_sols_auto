# syntax=docker/dockerfile:1

FROM python:3.9.2-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt
COPY cli_sols_auto /app/cli_sols_auto

RUN pip3 install -r requirements.txt && mkdir /app/in /app/out

ENTRYPOINT ["python", "cli_sols_auto/app.py"]
CMD ["--help"]
