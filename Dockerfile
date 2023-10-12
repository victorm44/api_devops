FROM python:3.11-alpine

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
RUN pip install mysql-connector-python

COPY  . /api

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
