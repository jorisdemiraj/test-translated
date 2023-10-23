from fastapi.testclient import TestClient
from server import app  
from src.rabbitmq.rabbitmq import message_broker

# create a TestClient instance with the FastAPI app
client = TestClient(app)

# start the message broker
message_broker.start()

# define a test for the statistics endpoint
def test_statistics():
    # send a GET request to the statistics endpoint
    response = client.get("/statistics")

    # assert that the response status code is 200
    assert response.status_code == 200

    # assert that the Output field in the response body is not empty
    assert response.json()["Output"] != {}

# define a test for the shorten_url endpoint
def test_shorten_url():
    # define the data to be sent in the POST request
    data = {
        "url": "http://example.com",  
        "email": "test@example.com"  
    }

    # send a POST request to the shorten_url endpoint with the data
    response = client.post("/short_url", data=data)

    # assert that the response status code is 200
    assert response.status_code == 200

    # assert that the content-type of the response is application/json
    assert response.headers["content-type"] == "application/json"

    # get the response body as JSON
    response_body = response.json()

    # assert that Output field exists in the response body
    assert "Output" in response_body

    # assert that short_url field exists in the Output field of the response body
    assert "short_url" in response_body["Output"]

    # assert that short_url starts with http://
    assert response_body["Output"]["short_url"].startswith("http://")

# define a test for the get_original_url endpoint
def test_get_original_url():
    url = "http://example.com"  

    # define the data to be sent in the POST request
    data = {
        "url": "http://example.com",  
    }

    # send a POST request to original_url endpoint with data
    response = client.post("/original_url", data=data)
    
    # assert that status code is either 200 or 404
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        # assert that content-type of response is application/json if status code is 200
        assert response.headers["content-type"] == "application/json"

        # get JSON from response body if status code is 200
        response_body = response.json()

        # assert Output field exists in JSON if status code is 200
        assert "Output" in response_body

        # assert url field exists in Output field of JSON if status code is 200
        assert "url" in response_body["Output"]

        # assert url field equals original url if status code is 200
        assert response_body["Output"]["url"] == url
