from kafka import KafkaConsumer
from kafka import TopicPartition
from flask import g
import logging

TOPIC_PEOPLE = 'persons'
TOPIC_LOCATIONS = 'locations'
CONSUMER_GROUP = 'udacity'
PARTITION = 0
KAFKA_SERVER = '10.43.126.236:9092'



consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER], enable_auto_commit=True,
                        consumer_timeout_ms=1000, auto_offset_reset='earliest')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-PEOPLE-API")

class ConsumerPersons:
    @staticmethod
    def get_all_persons():
        persons_dic_lst = consume(consumer, TOPIC_PEOPLE)

        return persons_dic_lst

class ConsumerLocations:
    @staticmethod
    def get_all_locations():
        persons_dic_lst = consume(consumer, TOPIC_LOCATIONS)

        return persons_dic_lst

def consume(consumer, topic):    
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])

    queue_entities = []
    for message_p in consumer:
        p_val = message_p.value.decode('UTF-8').strip('\"')
        queue_entities.append(p_val)

    #remove duplicates
    set(queue_entities)
    list(queue_entities)

    headers = queue_entities.pop(0)
    entities_dic_lst = []

    for val in queue_entities:
        entities_dict = {}
        for (i,j) in zip(val.split(", "), headers.split(", ")):
            entities_dict[j] = i
        entities_dic_lst.append(entities_dict)

    return entities_dic_lst
