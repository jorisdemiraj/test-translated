
# README

The task in hand is to design a simple multi-user program that manages the translation between a long URL and a short one. 

The approach is done through 2 Python Modules , communicating with each other through a RabbitMQ container.

There are 2 ways to run the project. 

- Through docker-compose to run the whole system 

- By running your own docker of RabbitMQ and Redis and starting the respective Client and Server python modules.

## Environment Variables

To run this project, depending on the chosen way of running, you will need to modify the following environment variables to both Client and Server .env file.

If the chosen method is to run your own docker RabbitMQ and Redis , you need to update the following variables:

`RABBIT_MQ_HOST = <your_rabbitmq_host>`

`REDIS_HOST = <your_redis_host>`

`REDIS_PORT = <your_redis_port>`

`REDIS_DB = <your_redis_db>`

On top of that you can declare your own Topic and Queue by modifying the variables:

`TOPIC` &
`QUEUE`

In addition, if chosen to run in local python module (non-docker), Client module requires absolute paths to be entered in [start_server.py](https://github.com/jorisdemiraj/test-translated/blob/main/Client/client/start_server.py) and [logconfig.ini](https://github.com/jorisdemiraj/test-translated/blob/main/Client/client/config/logconfig.ini) (commented line)



## Installation

To run in python module form (no docker) install the requirements.txt for both Client and Server. Note that the project requires Python. If Python is installed run the command to install the respective requirements.

```bash
  pip install -r requirements.txt
```


## Deployment

To deploy the dockerized version , open a terminal where the docker-compose.yaml file is and run the following command:

```bash
  docker-compose up 
```
Wait for the startup to finish.

Notes:

- The client-container will cycle in startup until RabbitMQ Docker is fully running. Once the RabbitMQ docker has started , it will correctly initialize itself and it will be fully operational with a log message: Application startup complete.

- The Client and Server components are capable of running separately in Docker if you wish to not use docker-compose. All containers deployed outside of docker-compose must fall under the same network and the Environmental Variables for the RabbitMQ and Redis Hosts must be updated to the service/cointainer name.

To deploy in python module form:

- For the Client, navigate to its directory and you can either run the command: 

```bash
  bash run.sh
``` 
which will deploy both the GUI and the Client , or to run just the Client without GUI: 

```bash
  python3 start_server.py
``` 

- For the server, navigate to its directory and run the command: 

```bash
  python3 main.py
``` 
## Demo

Once the deploy finishes there are two ways to test. 
- You can access the GUI using: http://localhost:8501/ which will give you an interactive website, fully built on python. It is advised to use the GUI due to the generation of graphs for the statistics functionality. ![App Screenshot](https://i.imgur.com/nqWCnVS.png)

- You can use any service similar to Postman, to send the requests. The default hostname of the client is http://0.0.0.0:22100 / http://localhost:22100

The endpoints are:

```bash
  POST: http://localhost:22100/short_url 
```
and takes an "url" and "email" for body
```bash
  POST: http://localhost:22100/original_url
```
with just an "url" for body
```bash
  GET:  http://localhost:22100/statistics
```


## Running Tests

Both Client and Server do include tests. To run tests,navigate to the tests directory and run the following command:

```bash
  pytest unit_test.py
```


## Acknowledgements

Thank you for your attention, and enjoy.
