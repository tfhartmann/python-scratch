#!//opt/boxen/homebrew/bin/python

import boto.sqs 
from boto.sqs.message import RawMessage
import json
import time 
import requests


REGION  = 'us-west-2'
QUEUE   = 'queuetest'
counter = 1

def queue_count( REGION, QUEUE):
    conn = boto.sqs.connect_to_region( REGION )
    q = conn.get_queue( QUEUE )
    count = q.count()
    return count 


def get_messages( REGION, QUEUE ):
    conn = boto.sqs.connect_to_region( REGION )
    q = conn.get_queue( QUEUE )
    mess = q.set_message_class(RawMessage)
    mess = q.get_messages()

    print 'Lenth ', len(mess)
    print 'Type ', type(mess) 

    for result in mess:
        print 'Hey >>>', type(result.get_body())
        rst = result.get_body()
        rst = json.loads(rst)
        url = rst['Message']
        r = requests.get(url)
        print r.json()
        print rst['Message']
        print rst['MessageId']
        q.delete_message(result)

while counter <= 5:
    if queue_count(REGION, QUEUE) > 0:
        print 'yup'
        get_messages(REGION, QUEUE)
        time.sleep(2)
        counter = counter + 1
        print counter
    else:
        print 'nope'
        time.sleep(10)
        counter = counter + 5
        print counter


#foo = {'FOO' : [ '12345678', '87654321' ], 'BAR' : [ '12345678', '87654321' ] } 
#print json.dumps(foo, indent=4, separators=(',', ': '))
#print json.dumps(foo)
