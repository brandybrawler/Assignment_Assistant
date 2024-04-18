import json
import sys
import time
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Job
import pika

SessionLocal = sessionmaker(bind=engine)

def process_job(job_data):
    # Placeholder for your job processing logic
    print("Processing job:", job_data)

def connect_to_rabbitmq():
    retries = 0
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials('123', '123')  # Modify with actual credentials
            ))
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            retries += 1
            if retries > 5:
                print("Failed to connect to RabbitMQ after several attempts.", file=sys.stderr)
                raise e
            sleep_time = min(2 ** retries, 30)  # Exponential backoff, capped at 30 seconds
            print(f"Connection failed, retrying in {sleep_time} seconds...", file=sys.stderr)
            time.sleep(sleep_time)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='job_queue')

def callback(ch, method, properties, body):
    job_data = json.loads(body)
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_data['job_id']).first()
        if job:
            job.status = 'completed'  # Update status based on actual processing outcome
            db.commit()
        process_job(job_data)
    finally:
        db.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='job_queue', on_message_callback=callback)
channel.start_consuming()
