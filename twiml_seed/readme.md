This python script will populate your new twiml table with working instructions.

Any number being called will be asked to press a key. After pressing a key, the caller will be directed to voicemail.

Replace \<email> in twiml.json with your email address. Replace \<table> in dynamo_insert.py with the table created by cloudformation. Then run python dynamo_insert from your computer. You will need boto installed and you will need to have an AWS profile that has privileges to the dynamo table that was created.