#!//opt/boxen/homebrew/bin/python

import boto.sns
import json


REGION = 'us-west-2'
TOPIC  = 'arn:aws:sns:us-west-2:473279429418:testtopic'
URL    = 'http://wwwdev-10wa.noc.harvard.edu/tunnels.json'

conn = boto.sns.connect_to_region( REGION )
pub = conn.publish( topic = TOPIC, message = URL )

#print json.dumps(foo, indent=4, separators=(',', ': '))
#print json.dumps(foo)
