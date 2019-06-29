This script answers a phone call from Twilio, requires the caller to enter a digit, then sends the caller to voicemail. 

It is easiest to install this script using code pipeline. Then direct your calls to the new API gateway URL via post. You will need to source from git, add a build phase, then install using cloudformation. If sourcing github, you will need to fork in order to setup the webhook on your repo. 

There is a separate seed script that provides the twiml instructions for the user to enter the digit and sends the caller to voicemail. Instructions are in the twiml_seed folder.

All DIDs must be properly formatted as +1NXXNXXNXXX - The script will first look for the did, then fall back to an asterisk, which will play for any DID. 
 
For steps with a number press, the digit pressed is before the hash, then the step- for example 1#1. For an incoming call with no digit press, it is the hash, followed by the step- #1. The script will first look for the actual digit pressed, then will fall back to any digit, *#1 

See https://www.twilio.com/docs/voice/twiml for a list of commands and the seed json file for an example of how to format your dynamo entries. I provide two new commands, 
gatherPlay(timeout,numDigits,url) which combines gather and play and
gatherSay(timeout,numDigits,txt) which combines gather and say.

@todo provide cloudformation for pipeline. 

@todo provide incoming SMS integration to block numbers.
