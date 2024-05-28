import pika

from prefect import task


def init_credentials(user, password):
    """"""
    credentials = pika.PlainCredentials(user, password)
    return credentials


@task(name="Init connection")
def init_connection(host, port, credentials):
    """"""
    vhost = "/"
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    connection = pika.BlockingConnection(parameters)
    return connection


@task(name="Init channel")
def init_channel(connection):
    """"""
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    return channel


@task(name="Declare queue")
def declare_queue(channel, queue, exchange):
    channel.queue_declare(queue=queue, durable=True)

    if exchange:
        channel.exchange_declare(exchange=exchange, exchange_type="direct")
        channel.queue_bind(exchange=exchange, queue=queue, routing_key=queue)


@task(name="Publish message")
def publish(channel, exchange, queue, message):
    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )
