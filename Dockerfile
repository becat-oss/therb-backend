FROM python:3.9-buster as base

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

RUN ["chmod","+x","entrypoint.sh"]

#ENTRYPOINT [ "entrypoint.sh" ]
CMD ["python","run.py"]