import os
from urllib.parse import parse_qs
import json
import boto3
from twilio.twiml.voice_response import VoiceResponse
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
blocked_table = dynamodb.Table(os.environ['blocked_table'])
twiml_table = dynamodb.Table(os.environ['twiml_table'])

class myVoiceResponse(VoiceResponse):

    def __getattr__(self,attr):
        try:
            return self.attr
        except Exception as e:
            try:
                return super().__getattr__(attr)
            except Exception as e:
                pass

    def gatherPlay(self,timeout=None,numDigits=None,url=None, **kwargs):
        return self.gather(input="dtmf", timeout=timeout, numDigits=numDigits).play(url)

    def gatherSay(self,timeout=None,numDigits=None,txt=None, **kwargs):
        return self.gather(input="dtmf", timeout=timeout, numDigits=numDigits).say(txt)
        
def lambda_handler(event, context):
    print(event)
    
    ret = {
        "statusCode": 200,
        "headers" : {
            "Content-Type": "application/xml"
        }
    }
    
    response = myVoiceResponse()
    
    body = event.get('body')
    if body == None:
        response.say("There was a problem with the call. Goodbye!")
        ret['body'] = str(response)
        return ret

    event_body = parse_qs(body)
    print(event_body)
    
    if 'Digits' in event_body:
        if event_body['Digits'][0]=='hangup':
            ret['body'] = str(response)
            return ret

    try:
        addons = event_body.get('AddOns',-1)[0]
        decoded = json.loads(addons)
        rep = decoded.get('results',-3).get('whitepages_pro_phone_rep',-4).get('result',-5).get('reputation_level',-6)
        if rep > 2:
            response.reject()
            ret['body'] = str(response)
            return ret
    except Exception as e:
        pass

    callerID = event_body.get('From')
    if callerID != None:
        r1 = blocked_table.query(
            KeyConditionExpression=Key('did').eq(callerID[0])
        )
        if len(r1['Items']) > 0:
            response.reject()
            ret['body'] = str(response)
            return ret

    did = event_body.get('Called',['*'])
    
    r2 = twiml_table.query(
        KeyConditionExpression=Key('did').eq(did[0])
    )
    exactCommands = []
    starCommands = []
    commands = []
    if did != '*' and len(r2['Items']) == 0:
        r2 = twiml_table.query(
            KeyConditionExpression=Key('did').eq('*')
        )
    if len(r2['Items']) == 0:
        response.say("There was a problem with the call. Goodbye!")
        ret['body'] = str(response)
        return ret
    for i in r2['Items']:
        itemarr = i['step'].split('#')
        if 'Digits' in event_body:
            if event_body['Digits'][0]==itemarr[0]:
                exactCommands.append(i)
            elif itemarr[0]=='*':
                starCommands.append(i)
        elif itemarr[0]=='':
            commands.append(i)
    if 'Digits' in event_body:
        if(len(exactCommands)):
            commands = exactCommands
        else:
            commands = starCommands
    for i in commands:
        command = i['command']
        params = i['params']
        try:
            getattr(response,command)(**params)
        except Exception as e:
            pass
        
    ret['body'] = str(response)
    return ret
