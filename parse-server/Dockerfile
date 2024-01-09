FROM python:alpine
WORKDIR /code

COPY ./*.py ./.env ./requirements.txt /code/
RUN apk add build-base linux-headers && \
    python -m pip install psutil && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8080
CMD ["uvicorn", "main:fast_api", "--host", "0.0.0.0", "--port", "8080"]
