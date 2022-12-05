FROM python:3.11-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache build-base jpeg-dev zlib-dev cargo
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8080"]