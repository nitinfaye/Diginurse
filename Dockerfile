FROM continuumio/anaconda3:4.4.0
COPY . /usr/flask_api/
EXPOSE 5000
WORKDIR /usr/flask_api/
RUN pip install -r requirements.txt 
CMD mongo
CMD rasa run --credentials credentials.yml
CMD rasa run actions
CMD python app.py
