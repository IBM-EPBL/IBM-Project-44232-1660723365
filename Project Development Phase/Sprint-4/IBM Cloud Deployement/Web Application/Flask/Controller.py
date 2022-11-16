from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

import requests

#model = pickle.load(open('./Final_CKD.pkl','rb'))
API_KEY = "hCHkzVPn1fJhWecbAOUWOG73U00EofIMTYUZLZiVEfv3"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}) 
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__,template_folder='template',static_folder='static')

@app.route('/')
def Home():
    return render_template("Home.html")

@app.route('/Home',methods=['POST','GET'])
def home():
    return render_template("Home.html")

@app.route('/Prdiction')
def Prediction():
    return render_template("Predict.html")

@app.route('/result',methods=["POST"])
def Predict():
    input_values = [float(i) for i in request.form.values()]
    feature_values = [np.array(input_values)]
    print("Feature values"+str(feature_values))
    feature_names = ['bu','bgr','cad','ane','pc','rbc','dm','pe']
    dataFrame = pd.DataFrame(feature_values,columns=feature_names)
    dataFrame= np.array(feature_values).reshape(1,-1)
    print("\nDataFrame"+str(dataFrame))

    #output = model.predict(dataFrame)
    payload_scoring = {"input_data": [{"field": [['bu','bgr','cad','ane','pc','rbc','dm','pe',]], "values": dataFrame.tolist()}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1c6ae6f6-61b8-48a4-8a84-d41e995b2bbb/predictions?version=2022-11-12', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    print((predictions['predictions'][0]['values'][0][0]))

    output = predictions['predictions'][0]['values'][0][0]
    if output==0:
        msg = "Regretful! You have a Chronic kidney disease"
        img = "../static/sad1.gif"
        return render_template('result.html',msg=msg,img=img)
    else:
        msg = "Hoorayyy! You don't have a chronic kidney disease"
        img="../static/happy1.gif"
        return render_template('result.html',msg=msg,img=img)


if __name__ == '__main__':
    app.run(debug=True)
