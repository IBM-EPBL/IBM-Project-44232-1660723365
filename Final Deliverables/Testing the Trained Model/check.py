import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "hCHkzVPn1fJhWecbAOUWOG73U00EofIMTYUZLZiVEfv3"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [['bu', 'bgr', 'cad','ane', 'pc', 'rbc','dm', 'pe',]], "values": [[10,140,0,0,1,1,0,0]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1c6ae6f6-61b8-48a4-8a84-d41e995b2bbb/predictions?version=2022-11-12', json=payload_scoring,
headers={'Authorization': 'Bearer ' + mltoken})
predictions = response_scoring.json()
print((predictions['predictions'][0]['values'][0][0]))