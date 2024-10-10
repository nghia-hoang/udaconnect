import os
import json

from datetime import datetime, timedelta

from kafka import KafkaConsumer

from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData, DateTime

from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Point

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = create_engine(DATABASE_URI)

meta = MetaData(db)  


location_table = Table('location', meta,  
                       Column('person_id', String),
                       Column('coordinate', Geometry("POINT",  srid=4326)),
                       Column('creation_time', DateTime))
                       

TOPIC_NAME = 'test'
KAFKA_HOST = '192.168.81.129'
KAFKA_PORT = 9092
KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

print("Consumer starting...")

with db.connect() as conn:
    for message in consumer:
        msg_data = json.loads(message.value)
        person_id = msg_data['person_id']
        longitude = msg_data['longitude']
        latitude = msg_data['latitude']
        creation_time =  datetime.strptime(msg_data['creation_time'],"%Y-%m-%d")

        # Create
        insert_statement = location_table.insert().values(person_id=person_id, coordinate=ST_Point(latitude, longitude), creation_time=creation_time)
        conn.execute(insert_statement)
