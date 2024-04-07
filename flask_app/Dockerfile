FROM python:3.9

WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENV PYTHONPATH="/flask_app:${PYTHONPATH}"

EXPOSE 5000

ENTRYPOINT ["python"]
CMD [ "wsgi.py"]
