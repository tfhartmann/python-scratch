#!//opt/boxen/homebrew/bin/python

import boto.sqs 
from boto.sqs.message import RawMessage
import json
import time 
import requests


REGION  = 'us-east-1'
QUEUE   = 'queuetest'
counter = 1

def create_queue( REGION, QUEUE):
    conn = boto.sqs.connect_to_region( REGION )
    q = conn.lookup( QUEUE ) 
    if q:
        print q
    else:
        print 'Sorry SQS Queue: ', QUEUE, 'Does not exist!'
        conn.create_queue( QUEUE )
        conn.add_permission( QUEUE , QUEUE, 'arn:aws:sns:us-east-1:473279429418:testtopic', 'SendMessage' )

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

create_queue(REGION, 'testfoo' )

while counter <= 5:
    count = queue_count(REGION, QUEUE)
    if count > 0:
        print 'yay! Message in Queue - lets do something! '
        print 'count in queue ', count 
        get_messages(REGION, QUEUE)
        time.sleep(2)
        counter = counter + 1
        print counter
    else:
        print 'nope, no messages move on dude...'
        time.sleep(10)
        counter = counter + 2
        print counter


#foo = {'FOO' : [ '12345678', '87654321' ], 'BAR' : [ '12345678', '87654321' ] } 
#print json.dumps(foo, indent=4, separators=(',', ': '))
#print json.dumps(foo)
