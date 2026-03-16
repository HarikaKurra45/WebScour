import pika
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()
channel.queue_declare(queue='url_queue', durable=True)

seed_url = input("Enter the seed url:")

print("Extracting links from seed URL...")

response = requests.get(seed_url)
soup = BeautifulSoup(response.text, "html.parser")

links = set()

for tag in soup.find_all("a", href=True):
    absolute_url = urljoin(seed_url, tag["href"])
    links.add(absolute_url)

print("Total links extracted:", len(links))


for link in links:
    channel.basic_publish(
        exchange='',
        routing_key='url_queue',
        body=link
    )

print("All extracted links sent to RabbitMQ.")

connection.close()
