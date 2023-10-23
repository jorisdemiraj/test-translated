from . import *

# set up logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# define a function to get a broker, and cache the result
@lru_cache()
def get_broker():
    return MessageBroker(RABBIT_MQ_HOST, TOPIC, QUEUE)

# define a class for the message broker that connects to RABBIT_MQ 
class MessageBroker:
    # initialize class variables
    host = ""
    topic = ""
    queue=""
    parameters=""
    producer = None
    channel= None
    corr_id=""
    queue_name=""
    consumer_tag=""
    response=None
    
    # constructor to initialize instance variables
    def __init__(self, host, topic,queue ):
        self.host = host
        self.topic = topic
        self.queue=queue
        self.parameters=  pika.ConnectionParameters(host,heartbeat=0)
        self.producer = pika.BlockingConnection(self.parameters)
        self.channel=  self.producer.channel()
    
    # method to start the broker
    def start(self):
        self.channel.queue_declare(queue=self.queue)
        self.channel.exchange_declare(exchange=self.topic, exchange_type='topic')
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.topic, queue=self.queue_name, routing_key='response')
        LOGGER.info(f"Connection to {self.queue} and {self.queue_name} started")

        
    # method to handle the message received
    def callback(self,ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)
            self.channel.basic_cancel(consumer_tag=self.consumer_tag)

    # method to start the consume process
    async def consume(self):
        
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True, consumer_tag=self.consumer_tag)
        self.channel.start_consuming()
        LOGGER.info(f"Consuming")

        
    # method to retrieve the response
    async def get_response(self):
        while self.response is None:
            await asyncio.sleep(0.5)
        return self.response
    
    # method to delete a queue (added just in case)
    def delete_queue(self,topic):
        self.channel.queue_delete(topic)
        
    # method to restart connection if needed
    def restart_connection(self):
        LOGGER.warn(f"Restarting Connection")
        self.producer = pika.BlockingConnection(self.parameters)
        self.channel=  self.producer.channel()
        self.start()
        
    
    # main function to send a message
    def send_msg(self, msg, uid):
        self.corr_id=uid
        self.consumer_tag=uid
        LOGGER.info(f"sending message to queue {self.queue} with message {msg}")
        try:
            # Send a message to the queue
            self.channel.basic_publish(exchange='', routing_key=self.queue, properties=pika.BasicProperties(reply_to='response',correlation_id=uid,
            ),body=msg)

        except Exception as ex:
            LOGGER.ERROR(ex)

            # if an exception occurs, restart the connection and try again
            self.restart_connection()
            self.channel.basic_publish(exchange='', routing_key=self.queue, properties=pika.BasicProperties(reply_to='response',correlation_id=uid,
            ),body=msg)

# get an instance of the broker    
message_broker = get_broker()
