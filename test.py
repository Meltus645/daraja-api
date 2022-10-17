import requests
from requests.auth import HTTPBasicAuth
import base64

url ="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
key ="oEQojWm3aLNaubr3kGGLsGl46VLifJRM" 
secret ="0Ry9FsbTFvkGzNPr"   
response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', auth=HTTPBasicAuth(key, secret), headers={'Content-Type': 'application/json'})
print(response.json())

