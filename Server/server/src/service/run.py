from . import *

# define a function to route the URL. Clicking on the short URL should call this function that will return the long URL and automatically redirect the user
def route_url(r,short_url):
    
    # parse the short URL to get the short code
    short_code= parse_url(short_url)
    
    try:
        # get the associated data from the database
        assoc= r.hgetall(short_code)
        # decode the URL from the associated data
        url= assoc['url'.encode()].decode('utf-8')
    except:
        # if an exception occurs, return None
        return None
    
    # return the decoded URL
    return url

# define a function to retrieve the original URL from a short URL version. It also increments count for the hit URL.
def retrieve_url(r,short_url):
    
    # parse the short URL to get the short code
    short_code= parse_url(short_url)
    
    try:
        # get the associated data from the database
        assoc= r.hgetall(short_code)
        # decode the URL from the associated data
        url= assoc['url'.encode()].decode('utf-8')
    except:
        # if an exception occurs, return None
        return None

    # if count is not in associated keys, set it to 1, else increment it by 1
    if 'count'.encode() not in assoc.keys():
        assoc['count'.encode()]=1
    else:
        assoc['count'.encode()]=int(assoc['count'.encode()])+1
        
    # set the updated associated data in the database
    r.hset(short_code, mapping=assoc)
    
    # return the decoded URL
    return url

# define a function to shorten a URL. It uses a hash code as identifier for hash table.
def shorten_url(r,url, email):
    
    # hash the URL using SHA256
    hash_object = hashlib.sha256(url.encode())
    
    # get hexadecimal representation of hash object
    hex_dig = hash_object.hexdigest()
    
    # get records associated with hexadecimal representation from database
    records = r.smembers(hex_dig)
    
    # convert records to list
    listed_records=list(records)

    if len(listed_records)>0:
        # if listed records exist, get short code from first record
        short_code=r.hget(listed_records[0].decode('utf-8'),'short_url').decode('utf-8')
    else:
        # else generate a new short code
        short_code = generate_short_code()
        
        # set url and short code in database
        r.set(url, short_code)
        
        # set email, url and short code in database with short code as key
        r.hset(short_code, mapping={'email': email, 'url': url, 'short_url': short_code})
        
        # add short code to set of hexadecimal representation in database
        r.sadd(hex_dig, short_code)
        
    # return short code
    return short_code

# define a basic statistics function
def statistics(r):
    
    keys = r.keys()
    email_counts = {}
    hash_counts = {}

    for key in keys:
        try:
            email = r.hget(key, 'email')
            count = r.hget(key, 'count')
        except:
            continue

        if email.decode('utf-8') in email_counts:
            email_counts[email.decode('utf-8')] += 1
        else:
            email_counts[email.decode('utf-8')] = 1

        if count is None:
            count=0

        hash_counts[URL_PATH+key.decode('utf-8')] = int(count)

    response= {
        "email_stat":email_counts,
        "url_stat":hash_counts
    }
    
    return response
