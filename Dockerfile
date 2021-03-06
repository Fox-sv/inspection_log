FROM python:3.9.6

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt


COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]