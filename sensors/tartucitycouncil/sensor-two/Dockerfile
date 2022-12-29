FROM python:slim-buster
WORKDIR /sensor-one-app
COPY . .
RUN pip3 install -r req.txt
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5001
ENTRYPOINT ["python", "app.py"]
