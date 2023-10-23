import pytest
import hashlib
from unittest.mock import MagicMock, patch
from src.service.run import shorten_url ,retrieve_url,statistics 
from config.load_settings import URL_PATH

# test function for shorten_url
@patch('redis.Redis')
def test_shorten_url(mock_redis):
    # create a mock Redis instance
    r = MagicMock()

    # define test url and email
    url = "http://example.com"
    email = "test@example.com"

    # mock the return value of smembers function
    r.smembers.return_value = []

    # define a test short code
    short_code = "abc123"

    # patch the generate_short_code function in the run module
    with patch('src.service.run.generate_short_code', return_value=short_code):  
        # call the shorten_url function and store the result
        result = shorten_url(r, url, email)

    # assert that the length of the result is equal to the length of the short code
    assert len(result) == len(short_code)

    # assert that the smembers, set, hset, and sadd functions were called with correct arguments
    r.smembers.assert_called_once_with(hashlib.sha256(url.encode()).hexdigest())
    r.set.assert_called_once_with(url, short_code)
    r.hset.assert_called_once_with(short_code, mapping={'email': email, 'url': url, 'short_url': short_code})
    r.sadd.assert_called_once_with(hashlib.sha256(url.encode()).hexdigest(), short_code)


# test function for retrieve_url
@patch('redis.Redis')
def test_retrieve_url(mock_redis):
    # create a mock Redis instance
    r = MagicMock()

    # define a test short url
    short_url = "http://example.com/abc123" 

    # define a test short code
    short_code = "abc123"

    # define a test association dictionary
    assoc = {
        'url'.encode(): 'http://original.com'.encode(),
        'count'.encode(): '0'.encode()
    }
    
    # mock the return value of hgetall function
    r.hgetall.return_value = assoc

    # patch the parse_url function in the run module
    with patch('src.service.run.parse_url', return_value=short_code):  
        # call the retrieve_url function and store the result
        result = retrieve_url(r, short_url)

    # assert that the result is equal to the decoded url in assoc dictionary
    assert result == assoc['url'.encode()].decode()

    # assert that the hgetall and hset functions were called with correct arguments
    r.hgetall.assert_called_once_with(short_code)
    r.hset.assert_called_once_with(short_code, mapping=assoc)
    
    
# test function for statistics
@patch('redis.Redis')
def test_statistics(mock_redis):
    # create a mock Redis instance
    r = MagicMock()

    # define a list of test keys
    keys = ['key1'.encode('utf-8'), 'key2'.encode('utf-8')]

    # mock the side effect of hget function 
    r.hget.side_effect = ['email1'.encode('utf-8'), '1', 'email2'.encode('utf-8'), '2']

    # mock the return value of keys function 
    r.keys.return_value = keys

     # call the statistics function and store the result
    result = statistics(r)

     # define expected result dictionary 
    expected_result = {
         "email_stat": {'email1': 1, 'email2': 1},
         "url_stat": {URL_PATH + 'key1': 1, URL_PATH + 'key2': 2}
     }

     # assert that the result is equal to expected_result dictionary 
    assert result == expected_result

     # assert that keys and hget functions were called with correct arguments 
    r.keys.assert_called_once()
    r.hget.assert_any_call('key1'.encode('utf-8'), 'email')
    r.hget.assert_any_call('key1'.encode('utf-8'), 'count')
    r.hget.assert_any_call('key2'.encode('utf-8'), 'email')
    r.hget.assert_any_call('key2'.encode('utf-8'), 'count')
