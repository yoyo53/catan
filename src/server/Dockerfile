FROM python:3.10-slim AS build

RUN apt-get update && apt-get install -y build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ADD ./server/requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10-alpine AS run

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

ADD ./server ./server
ADD ./lib ./lib

WORKDIR ./server
CMD python WebsocketServer.py