# Test cases:
# Add only address. #204
# Add incorrect address #400 Bad Request
# Add address multiple times. #400 Bad Request
# Add customer with new address. #204
# Add customer multiple times. #400 Bad Request
# Add customer with already existing address. #204
# Add customer without address.- Not sure how to take care of this. Maybe the address could be updates in put.#204
# Add customer with incorrect address. #400 Bad request
# Add incorrect customer email. #400 bad request

from __future__ import print_function

import urllib2
import urllib
import json
import boto3
import re
import random

def respond(err, res=None, error_code = 204):
    response =  {}
    
    if err:
        response['statusCode'] = str(error_code)
        response['body'] = err.message
    else:
        response['status'] = str(204)
        response['body'] = res
    
    response['headers'] = {'Content-Type': 'application/json',}
    
    return response

def lambda_handler(event, context):
    '''Creates a new entry for the group.
        '''
    try:
        table = boto3.resource('dynamodb')
        gp = table.Table('GroupPasswords')
        groupId = random.randint(0, 10000)
        while(True):
            value = gp.get_item(Key={'groupId' : groupId})
            if('Item' not in value):
                break;
            groupId = random.randint(0, 10000)
        
        groupPassword = random.randint(12345678, 99999999999)
        new_item = {}
        if('context' in event):
            item = event['context']
            if('cognito-identity-id' in item):
                userId = item['cognito-identity-id']
                if(userId != ""):
                    new_item['moderator'] = userId
    
        new_item['groupId'] = groupId
        new_item['password'] = groupPassword
        gp.put_item(Item=new_item)
    return respond(None, {'message':'GroupId:'+ str(groupId) + ' Password:' + str(groupPassword)})
except:
    return respond(ValueError('Invalid request.'), None, 400)
