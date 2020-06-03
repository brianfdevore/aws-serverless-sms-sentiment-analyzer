import json
import urllib.parse as urlparse
import boto3

# import requests


def lambda_handler(event, context):
    body = event["body"]
    print(body)
    parsed = urlparse.parse_qs(body)
    text = parsed["Body"][0]
    print(text)

    client = boto3.client('comprehend')
    
    s_response = client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = s_response['Sentiment']

    e_response = client.detect_entities(Text=text, LanguageCode='en')
    
    people = ''
    locations = ''
    orgs = ''
    items = ''
    events = ''
    dates = ''
    qtys = ''
    titles = ''
    other = ''
    
    for entity in e_response["Entities"] :
        #entities += entity["Type"] + ': ' + entity["Text"] + '\n'
        
        if entity["Type"] == 'PERSON' :
            people += entity["Text"] + ', '
            
        if entity["Type"] == 'LOCATION' :
            locations += entity["Text"] + ', '
            
        if entity["Type"] == 'ORGANIZATION' :
            orgs += entity["Text"] + ', '
            
        if entity["Type"] == 'COMMERCIAL_ITEM' :
            items += entity["Text"] + ', '
            
        if entity["Type"] == 'EVENT' :
            events += entity["Text"] + ', '
            
        if entity["Type"] == 'DATE' :
            dates += entity["Text"] + ', '
            
        if entity["Type"] == 'QUANTITY' :
            qtys += entity["Text"] + ', '
            
        if entity["Type"] == 'TITLE' :
            titles += entity["Text"] + ', '
            
        if entity["Type"] == 'OTHER' :
            other += entity["Text"] + ', '
            


    return {
        "statusCode": 200,
        "body": '<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Sentiment: ' + sentiment + '\nPeople: ' + people + '\nLocations: ' + locations + '\nOrgs: ' + orgs + '\nItems: ' + items + '\nEvents: ' + events + '\nDates: ' + dates + '\nQtys: ' + qtys + '\nTitles: ' + titles + '\nOther: ' + other + '</Body></Message></Response>',
        "headers": {"Content-Type": "application/xml"}
    }
