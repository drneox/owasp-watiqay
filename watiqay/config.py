from sys import path
from mongoengine import connect

'''
Basic config file for watiqay server
'''

# Config mailgun api (mailgun.com)
EMAIL = 'watiqay@watiqay.org'
API = 'key-3ax6xnjp29jd6fds4gc373sgvjxteol0'
DOMAIN = 'samples.mailgun.org'


# Scan interval in seconds. default: 60 seconds(1 min.)
INTERVAL_SCANNING = 1
# Repeated log interval in minutes
# change this time if you want to receive repeated log more often
INTERVAL_LOG = 30
# project path add to python path
path.append(__file__)
# DB conection
connect('watiqay')
