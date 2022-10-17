from os import getenv
from flask import request, url_for
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
    # phone number and amount 
    form =request.form
    phone =form.get('phone')
    amount =form.get('amount')
    access_token:str =get_access_token() 
    ENDPOINT =getenv('ENDPOINT') # stk push request endpoint
    BUSINESS_SHORTCODE =getenv('BUSINESS_SHORTCODE')
    headers ={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}  # send access token in request headers
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S") 
    password = f"{174379}MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwOTIzMTI0NjA1{timestamp}" 
    request_body = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": base64.b64encode(password.encode()).decode(),
        "Timestamp": timestamp, 
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": url_for('daraja.callback'),
        "AccountReference": "SAFETY4YOU",
        "TransactionDesc": "registration"
    }
    stk_push_request =requests.post(ENDPOINT, json=request_body, headers=headers)
    stk_push_json_response =stk_push_request.json()
    return stk_push_json_response 

def register(): 
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    access_token = get_access_token()
    my_endpoint ="c2b/"
    headers = { "Authorization": "Bearer %s" % access_token }
    r_data = {
        "ShortCode": "600383",
        "ResponseType": "Completed",
        "ConfirmationURL": my_endpoint + 'con',
        "ValidationURL": my_endpoint + 'val'
    }

    response = requests.post(endpoint, json=r_data, headers=headers)
    return response.json()

def callback():
    data =request.get_json()
    try:
        with open(BASEDIR /'data.json', 'a') as data_file: data_file.write(data)
        response ={'message': 'data saved successfully'}
    except Exception as e: response ={'detail': f'error saving data {e}'}
    finally: return response  

