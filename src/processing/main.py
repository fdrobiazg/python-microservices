import os, pika
from utils import clr2gray
from pymongo import MongoClient
import gridfs

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
SVC_QUEUE = os.environ.get("SVC_QUEUE")

def main():
    mongo = MongoClient(MONGO_HOST,
                     username=MONGO_USER,
                     password=MONGO_PASSWORD,
                     authSource='admin')
    
    src_gfs = gridfs.GridFS(mongo['src_img'])
    out_gfs = gridfs.GridFS(mongo['processed_img'])

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = clr2gray.convert(body, src_gfs, out_gfs, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=SVC_QUEUE, on_message_callback=callback
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()