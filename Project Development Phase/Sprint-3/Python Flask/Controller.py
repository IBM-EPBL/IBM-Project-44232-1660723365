from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

model = pickle.load(open('./Final_CKD.pkl','rb'))

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
    print(feature_values)
    feature_names = ['bu','bgr','cad','ane','pc','rbc','dm','pe']
    dataFrame = pd.DataFrame(feature_values,columns=feature_names)
    dataFrame= np.array(dataFrame).reshape(1, -1)

    output = model.predict(dataFrame)
    print(output[0])
    if output==0:
        msg = "Sorry to say! You have a Chronic kidney disease"
        img = "../static/sad1.gif"
        return render_template('result.html',msg=msg,img=img)
    else:
        msg = "Don't worry!"
        img="../static/happy1.gif"
        return render_template('result.html',msg=msg,img=img)


if __name__ == '__main__':
    app.run(debug=True)
