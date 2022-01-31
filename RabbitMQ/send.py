from multiprocessing import connection
import queue
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello Abhijith!')

print("[x] Sent 'Hello Abhijith!'")

connection.close()