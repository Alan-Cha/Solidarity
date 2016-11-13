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
from boto3.dynamodb.conditions import Key, Attr
import math
import decimal
from datetime import datetime, timedelta


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

def call_microsoft_locations(longitude, latitude):
    key = "AlTEVvX26IpywdL-bI5p18oBd8ydEj1j9yd82cGVITs2NUnvwDENsN5IsGKe8U1_"
    url = "http://dev.virtualearth.net/REST/v1/Locations/%f,%f?key=%s"%(longitude, latitude, key)
    print(url)
    content = json.loads(urllib2.urlopen(url).read())
    
    print(content)
    resourceSet = content['resourceSets']
    item = resourceSet[0]
    res = item['resources']
    resource = res[0]
    address = resource['address']
    addStr = address['formattedAddress']
    return addStr

#function to calculate distance between two points with longitude and latitude
def distance(lat1, long1, lat2, long2):
    dlong = math.fabs(long1-long2)
        dlat = math.fabs(lat1-lat2)
            dist = math.sqrt(dlong*dlong+dlat*dlat)
                return dist

def lambda_handler(event, context):
    '''Creates a new entry for the group.
        '''
    
    try:
        table = boto3.resource('dynamodb')
        groupIdTable = table.Table('solidarity-mobilehub-1621301408-GroupUser')
        locationsTable = table.Table('solidarity-mobilehub-1621301408-Locations')
        messageTable = table.Table('solidarity-mobilehub-1621301408-panicMessages')
        if 'body-json' not in event:
            return respond(ValueError('Invalid PUT request'), None, 400)
        print("past if")
        
        item = event['body-json']
        
        longitude = decimal.Decimal(item['longitude'])
        
        latitude = decimal.Decimal(item['latitude'])
        
        messageaddress = call_microsoft_locations(latitude, longitude)
        print(messageaddress)
        if item.has_key('userId'):
            userId = item['userId']
        else:
            context = event['context']
            print(item)
            userId = context['cognito-identity-id']
print('userId: ' + userId)
    
    # fe = Key('year').between(1950, 1959);
    #     pe = "#yr, title, info.rating"
    #     # Expression Attribute Names for Projection Expression only.
    #     ean = { "#yr": "year", }
    #     esk = None
    
    # response = table.scan(
    #     FilterExpression=fe,
    #     ProjectionExpression=pe,
    #     ExpressionAttributeNames=ean
    # )
    
    response = groupIdTable.query(
                                  ProjectionExpression = "groupId",
                                  KeyConditionExpression = Key('userId').eq(userId)
                                  )
        print(response)
        
        groupsId = []
        for item in response['Items']:
            groupsId.append(int(item['groupId']))
        print (groupsId)
        print (type(groupsId[0]))
        
        
        
        alliesId = []
        alliesHash = []
        for groupId in groupsId:
            response = groupIdTable.query(
                                          ProjectionExpression = 'userId',
                                          IndexName = 'groupId',
                                          KeyConditionExpression = Key('groupId').eq(groupId)
                                          )
        
        for item in response['Items']:
            alliesId.append(item['userId'])

#Convert the response above into an array of userIds named allies

for allyId in alliesId:
    response = locationsTable.query(
                                    ProjectionExpression = "latitude, longitude",
                                    KeyConditionExpression = Key('userId').eq(allyId)
                                    )
        
        tempHash = {}
            tempHash['userId'] = allyId
            
            # Check this!!!
            temparray = response['Items']
            tempitem = temparray[0]
            tempHash['latitude'] = tempitem['latitude']
            tempHash['longitude'] = tempitem['longitude']
            alliesHash.append(tempHash)
        
        print(alliesHash)
        newHash = []
        for allyHash in alliesHash:
            threshold = 50
            if distance(longitude, latitude, allyHash['longitude'], allyHash['latitude']) > threshold:
                newHash.append(allyHash)
        print(newHash)

        loc_dt = str(datetime.utcnow())
        
        for item in newHash:
            messageTable.put_item(Item={'userId':item['userId'],'time':loc_dt, 'address':messageaddress})

                return respond(None, {'message':'Panic message sent'})
except:
    return respond(ValueError('Invalid request.'), None, 400)
