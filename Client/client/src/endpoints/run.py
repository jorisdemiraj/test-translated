from . import *

# initialize logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# endpoint to retrieve statistics
@router.get(
    "/statistics",
    response_model=RunInResponseInComputing,
    tags=["test"],
    status_code=HTTP_202_ACCEPTED,
    summary="Create a new run using ssi method.",
    description="Create a new run based on stochastic subspace identification analysis."
)
async def get_statistics():  
    
    request= {}
    # create a unique id for the request
    hash_object = hashlib.sha256("statistics".encode())
    hex_dig = hash_object.hexdigest()
    
    request['id']=hex_dig
    request['ack']=False
    request['type']="statistics"

    # send the request to the message broker
    message_broker.send_msg(json.dumps(request), hex_dig)    
    
    # wait for the response from the message broker
    await message_broker.consume()

    response = await message_broker.get_response()

    return create_aliased_response({"Output": response})

# endpoint to convert a long url into a short url
@router.post(
    "/short_url",
    response_model=RunInResponseInComputing,
    tags=["test"],
    status_code=HTTP_202_ACCEPTED,
    summary="Create a new run using ssi method.",
    description="Create a new run based on stochastic subspace identification analysis."
)
async def shorten_url(
        url:  str = Form(...),
        email: str = Form(...)

):  
    request= {}
    
    # create a unique id for the request
    hash_object = hashlib.sha256(str(url).encode())
    hex_dig = hash_object.hexdigest()
    
    request['url']=url
    request['email']=email
    request['id']=hex_dig
    request['ack']=False
    request['type']="convert"

    LOGGER.info(f"Calling send request")

    # send the request to the message broker
    message_broker.send_msg(json.dumps(request), hex_dig)    
    
    LOGGER.info(f"awaiting consume")
    # wait for the response from the message broker
    await message_broker.consume()
    
    LOGGER.info(f"awaiting response")

    response = await message_broker.get_response()
    
    # append host and port to the short url
    response['short_url']= 'http://'+APP_HOST+':'+ APP_PORT+'/'+response['short_url']
    
    return create_aliased_response({"Output": response})

# endpoint to retrieve original long url from short url
@router.post(
    "/original_url",
    response_model=RunInResponseInComputing,
    tags=["test"],
    status_code=HTTP_202_ACCEPTED,
    summary="Create a new run using ssi method.",
    description="Create a new run based on stochastic subspace identification analysis."
)
async def get_original_url(
        url:  str = Form(...)

):  
    request= {}
    
    # create a unique id for the request
    hash_object = hashlib.sha256(str(url).encode())
    hex_dig = hash_object.hexdigest()
    
    request['url']=url
    request['id']=hex_dig
    request['ack']=False
    request['type']="retrieve"

    # send the request to the message broker
    message_broker.send_msg(json.dumps(request), hex_dig)
   
    # wait for the response from the message broker
    await message_broker.consume()

    response = await message_broker.get_response()
    
    # check if the url is valid, if not return an error message
    if response['url'] is None:
        return create_aliased_response(
        {"URL is not recognisable."}, status_code=HTTP_404_NOT_FOUND)
    
    return create_aliased_response({"Output": response})

# endpoint to redirect to original url when clicking on the short url
@router.get('/{short_code}')
async def redirect_to_url(short_code:  str = Path(..., min_length=1)):
    
    request= {}
    
    # create a unique id for the request
    hash_object = hashlib.sha256(str(short_code).encode())
    hex_dig = hash_object.hexdigest()
    
    request['url']=short_code
    request['id']=hex_dig
    request['ack']=False
    request['type']="route"

    # send the request to the message broker
    message_broker.send_msg(json.dumps(request), hex_dig)    
    
    # wait for the response from the message broker
    await message_broker.consume()

    response = await message_broker.get_response()
    
    # get the original url from the response
    url= response['url']
    
    # check if the url is valid, if not return an error message
    if url is None:
        return create_aliased_response({"ERROR:404": "URL is not recognisable."})
    
    else:
        # redirect to the original url
        return RedirectResponse(url=url)
