import os
from urlparse import parse_qs
import xml.etree.cElementTree as ET

def gatherSay(t,d,txt):
    gather = ET.Element("Gather",input="dtmf", timeout=t, numDigits=d)
    Say = ET.SubElement(gather,"Say").text=txt
    return gather

def record(email):
    callback = "http://twimlets.com/voicemail?Email={}".format(email)
    rec = ET.Element("Record",timeout="10", transcribe="true",maxLength="20",transcribeCallback=callback)
    return rec

def lambda_handler(event, context):
    print event
    
    ret = {
        "statusCode": 200,
        "headers" : {
            "Content-Type": "application/xml"
        }
    }
    
    response = ET.Element("Response")
    
    if event['body'] != None:
        event_body = parse_qs(event['body'])
        print event_body
        if 'Digits' in event_body:
            ET.SubElement(response,"Say").text="Please wait while I connect your call."
            ET.SubElement(response,"Play").text="https://alcoholic-reaction-4540.twil.io/assets/moh.wav"
            ET.SubElement(response,"Say").text="The person you called is not available. Please leave your message at the beep."
            response.append(record(os.environ['email']))
            ret['body'] = ET.tostring(response)
            return ret
        else:
            response.append(gatherSay("5","1","We do not recognize your number. Press 1 to verify you are human."))
            response.append(gatherSay("5","1","We do not recognize your number. Press 1 to verify you are human."))
            ET.SubElement(response,"Say").text="We did not receive any input. Goodbye!"
            ret['body'] = ET.tostring(response)
            return ret
            
    else:
        ET.SubElement(response,"Say").text="There was a problem with the call. Goodbye!"
        ret['body'] = ET.tostring(response)
        return ret
