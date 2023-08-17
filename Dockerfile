FROM python:3.11-alpine

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY  main.py /api

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]