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
        gu = table.Table('solidarity-mobilehub-1621301408-Locations')
        if 'body-json' not in event:
            return respond(ValueError('Invalid PUT request'), None, 400)
        
        item = event['body-json']
        context = event['context']
        print(item)
        userId = context["cognito-identity-id"]
        print("userId: " + userId)
        
        longitude = item["longitude"]
        print('longitude: ' + str(longitude))
        
        latitude = item["latitude"]
        print('latitude: ' + str(latitude))
        
        gu.delete_item(Key={'userId': userId})
        
        new_item = {
            'userId': userId,
            'longitude': longitude,
            'latitude': latitude
        }
        
        gu.put_item(Item=new_item)
        
    return respond(None, {'message':'Successful Join'})
except:
    return respond(ValueError('Invalid request.'), None, 400)
