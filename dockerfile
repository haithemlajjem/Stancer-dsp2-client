FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv build

RUN pip install dist/*.whl

CMD ["python"]
