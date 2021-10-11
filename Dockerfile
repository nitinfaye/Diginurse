ENTRYPOINT []
RUN apt-get update && apt-get install - pip3 install --no-cache rasa==1.10.8 --use-feature=2020-resolver
ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh



FROM continuumio/anaconda3:4.4.0
COPY . /usr/flask_api/
EXPOSE 5000
WORKDIR /usr/flask_api/
RUN pip install -r requirements.txt 
CMD mongoDB
CMD rasa run --credentials credentials.yml
CMD rasa run actions
CMD python app.py
