# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('sid')
auth_token = os.getenv('tok')
print(account_sid,auth_token)
# client = Client(account_sid, auth_token)

def sendMessage(name,number,data):
    #  message = client.messages \
    #             .create(
    #                  body=f'''Hello {name}, you student was present in class
    #                      for {data['days']} and is presence is {data['presence']}%''',
    #                  from_='+16503380654',
                    #  to='+91' + str(number)
                #  )
    print("IMP")

# sendMessage("Boss",6206934587,{
#     'days':30,'presence': 100
# })
# print(message.sid)

