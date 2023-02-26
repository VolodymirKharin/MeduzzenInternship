FROM python:3.10
COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r requirements.txt
WORKDIR /code
COPY . .
EXPOSE 8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
