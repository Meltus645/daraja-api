from os import getenv
from flask import request 
import base64, requests
from datetime import datetime
from requests.auth import HTTPBasicAuth 
from dotenv import load_dotenv
from app.utils.constants import BASEDIR

load_dotenv()
def get_access_token()->str: # get access token from M-PESA
    CONSUMER_KEY:str =getenv('CONSUMER_KEY')
    CONSUMER_SECRET:str =getenv('CONSUMER_SECRET')
    API_URL:str =getenv('API_URL') 
    access_token_response:requests.Response =requests.get(API_URL, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET), headers={'Content-Type': 'application/json'}) 
    response_json =access_token_response.json()
    access_token =response_json['access_token']
    return access_token 
     
 
def init_push():
    try:
        # phone number and amount 
        form =request.form
        phone =form.get('phone')
        amount =form.get('amount')
        access_token:str =get_access_token() # get the access token here
        ENDPOINT =getenv('ENDPOINT') # stk push request endpoint
        BUSINESS_SHORTCODE =getenv('BUSINESS_SHORTCODE') # shortcode
        PASSKEY =getenv('PASSKEY') # pass key
        headers ={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}  # send access token in request headers
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S") # timestamp yyyymmddhhMMss
        password = f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}"  # generate passwoerd from shortcode, passkey and timestamp
       
        # stk push request body and parameters
        request_body = {
            "BusinessShortCode": BUSINESS_SHORTCODE,
            "Password": base64.b64encode(password.encode()).decode(),
            "Timestamp": timestamp, 
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": BUSINESS_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": 'https://daraja-api-flask.herokuapp.com/daraja/callback', # TODO: change me
            "AccountReference": "SAFETY4YOU",
            "TransactionDesc": "registration"
        }
        stk_push_request =requests.post(ENDPOINT, json=request_body, headers=headers)
        stk_push_json_response =stk_push_request.json() 
        return {
            'success': True,
            'detail': stk_push_json_response
        }
    except:
        return {
            'success': False,
            'detail': 'Failed please try again'
        }
 

def callback(): 
    data =request.get_json()
    try:
        with open(BASEDIR /'data.json', 'a') as data_file: data_file.write(data)
        response ={
            'success': True,
            'message': 'data saved successfully'
        }
    except Exception as e: response ={
        'success': False,
        'detail': f'error saving data {e}'
    }
    finally: return response  

