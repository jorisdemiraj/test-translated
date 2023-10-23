from . import *

# declare a class for the RABBITMQ Consumer
class MessageConsumer(object):
    
    # initialize class variables
    host = ""
    topic = ""
    queue=""
    parameters=""
    producer = None
    channel= None
    corr_id=""
    r=None
    
    # constructor to initialize instance variables
    def __init__(self, host, topic,queue ):
        self.host = host
        self.topic = topic
        self.queue= queue
        self.parameters=  pika.ConnectionParameters(host,heartbeat=60)
        self.producer = pika.BlockingConnection(self.parameters)
        self.channel=  self.producer.channel()
        
    # method to start the consumer and declare a basic consume
    def start(self,r):
        self.r=r
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_request)
    
    # method to restart connection if needed
    def restart_connection(self):
        self.producer = pika.BlockingConnection(self.parameters)
        self.channel=  self.producer.channel()
        self.start()
        
    # method to handle the packets that come in
    def on_request(self, ch, method, props, body):
        
        # process the payload
        print("Received request: %r" % body)

        response=json.loads(body)
        
        
        send_response={}
        try:
            typeRequest=response['type']
            if typeRequest=='convert':
                
                url=response['url']
                email=response['email']
                
                shorturl=shorten_url(self.r,url,email)
                
                send_response['short_url']=shorturl
            
            elif typeRequest=='retrieve':
                
                short_url=response['url']
                
                url=retrieve_url(self.r,short_url)
                
                send_response['url']=url
            
            elif typeRequest=='route':
                
                short_url=response['url']
                
                url=route_url(self.r,short_url)
                
                send_response['url']=url
            
            elif typeRequest=='statistics':
                
                send_response=statistics(self.r)
                
            if not response['ack']:
                
                send_response['id']=response['id']
                send_response['ack']=True
        except:
            response = json.dumps(send_response)
        
        # stringify payload and send to the topic
        
        response = json.dumps(send_response)
        
        ch.basic_publish(exchange=self.topic,
                         routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # method to start actively consuming
    def start_consume(self):
        print("Awaiting requests")
        self.channel.start_consuming()
