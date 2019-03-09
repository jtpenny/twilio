import boto3 
import json
import os
from urlparse import parse_qs
def lambda_handler(event, context):
    print event
    if event['body'] != None:
        event_body = parse_qs(event['body'])
        print event_body
        if 'Digits' in event_body:
            myValues = {
                'email':os.environ['email']
            }
            return {
                    "statusCode": 200,
                    "headers" : {
                        "Content-Type": "application/xml"
                    },
                    "body": """<Response>
                                    <Say>Please wait while I connect your call.</Say>
                                    <Play>https://alcoholic-reaction-4540.twil.io/assets/moh.wav</Play>
                                    <Say>The person you called is not available. Please leave your message at the beep.</Say>
                                    <Record timeout="10" transcribe="true" transcribeCallback="http://twimlets.com/voicemail?Email=%(email)s" maxLength="20" />
                                </Response>""" % myValues
                   
                }
        else:    
            return {
                    "statusCode": 200,
                    "headers" : {
                        "Content-Type": "application/xml"
                    },
                    "body":"""<Response>
                                    <Gather input="dtmf" timeout="5" numDigits="1">
                                        <Say>We do not recognize your number. Press 1 to verify you are human.</Say>
                                    </Gather>
                                    <Gather input="dtmf" timeout="5" numDigits="1">
                                        <Say>We do not recognize your number. Press 1 to verify you are human.</Say>
                                    </Gather>
                                    <Say>"We didn't receive any input. Goodbye!"</Say>
                                </Response>"""
                   }
    else:
        return {
                    "statusCode": 200,
                    "headers" : {
                        "Content-Type": "application/xml"
                    },
                    "body":"""<Response>
                                    <Say>"There was a problem with the call. Goodbye!"</Say>
                                </Response>"""
        }
