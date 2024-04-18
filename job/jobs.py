import pika
import json
import time
import sys

def process_job(job_data):
    # Logic to process job
    print("Processing job:", job_data)

def connect_to_rabbitmq():
    retries = 0
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials('123', '123')
            ))

            return connection
        except pika.exceptions.AMQPConnectionError as e:
            retries += 1
            if retries > 5:
                print("Failed to connect to RabbitMQ after several attempts.", file=sys.stderr)
                raise e
            sleep_time = min(2 ** retries, 30)  # Exponential backoff capped at 30 seconds
            print(f"Connection failed, retrying in {sleep_time} seconds...", file=sys.stderr)
            time.sleep(sleep_time)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='job_queue')

def callback(ch, method, properties, body):
    job_data = json.loads(body)
    process_job(job_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='job_queue', on_message_callback=callback, auto_ack=False)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
