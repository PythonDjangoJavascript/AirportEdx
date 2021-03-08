FROM python:3.9
COPY . /usr/src/edx/app
WORKDIR /usr/src/edx/app
RUN pip3 install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]