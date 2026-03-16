import pika
import requests
import os

os.makedirs("pages", exist_ok=True)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='url_queue', durable=True)


channel.basic_qos(prefetch_count=1)

page_count = 1

def callback(ch, method, properties, body):
    global page_count

    url = body.decode()
    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        existing_files = len(os.listdir("pages")) + 1
        filename = f"pages/page_{existing_files}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Saved: {filename}")
        page_count += 1

    except:
        print("Error fetching:", url)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue='url_queue',
    on_message_callback=callback
)

print("Worker started...")
channel.start_consuming()

