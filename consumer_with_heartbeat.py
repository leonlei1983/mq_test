import pika
import time

param = pika.ConnectionParameters(
    host='localhost',
    heartbeat=10,
    # heartbeat_interval=120, # 0.10.0
)
connection = pika.BlockingConnection(param)
channel = connection.channel()


channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):

    current_time = time.time()
    now = time.ctime(int(current_time))
    print("%s [x] Received %r" % (now, body))

    for idx in range(6):
        print("sleep 5 secs")
        time.sleep(5)
        connection.process_data_events()

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
