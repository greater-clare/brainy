# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=7860" ]