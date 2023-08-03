# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 19:50:53 2023

@author: Rahul Nakka
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import datetime
app = Flask(__name__)
model = pickle.load(open('random_forest_regression.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        #Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        
        Owner_Second=request.form['Owner']
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']#7207916415
        #<!--Colour=int(request.form['Colour'])-->
        Length=int(request.form['Length'])
        Fuel_Capacity=int(request.form['Fuel_Capacity'])
        
        if(Owner_Second=='Second'):
            Owner_Second=1	
            Owner_Third	=0
            Owner_UnRegisteredCar=0
        elif(Owner_Second=='Third'):
            Owner_Second=0	
            Owner_Third	=1
            Owner_UnRegisteredCar=0
        elif(Owner_Second=='UnRegistered Car'):
            Owner_Second=0	
            Owner_Third	=0
            Owner_UnRegisteredCar=1
        else:
            Owner_Second=0	
            Owner_Third	=0
            Owner_UnRegisteredCar=0
        
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_CC=0
                Fuel_Type_LPG=0
                Fuel_Type_Hybrid=0
                Fuel_Type_PC=0      
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Type_CC=0
            Fuel_Type_LPG=0
            Fuel_Type_Hybrid=0
            Fuel_Type_PC=0
        elif(Fuel_Type_Petrol=='CNG + CNG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CC=1
            Fuel_Type_LPG=0
            Fuel_Type_Hybrid=0
            Fuel_Type_PC=0
        elif(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CC=0
            Fuel_Type_LPG=1
            Fuel_Type_Hybrid=0
            Fuel_Type_PC=0
        elif(Fuel_Type_Petrol=='Hybrid'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CC=0
            Fuel_Type_LPG=0
            Fuel_Type_Hybrid=1
            Fuel_Type_PC=0
        elif(Fuel_Type_Petrol=='Petrol + CNG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CC=0
            Fuel_Type_LPG=0
            Fuel_Type_Hybrid=0
            Fuel_Type_PC=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CC=0
            Fuel_Type_LPG=0
            Fuel_Type_Hybrid=0
            Fuel_Type_PC=0
        Year=datetime.date.today().year-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Corporate=0
        elif (Seller_Type_Individual=='Corporate'):
            Seller_Type_Corporate=1
            Seller_Type_Individual=0	
        else:
            Seller_Type_Corporate=0
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Kms_Driven,Length,Fuel_Capacity,Year,Fuel_Type_CC,Fuel_Type_Diesel,Fuel_Type_Hybrid,Fuel_Type_LPG,Fuel_Type_Petrol,Fuel_Type_PC,Transmission_Mannual,Owner_Second,Owner_Third,Owner_UnRegisteredCar,Seller_Type_Corporate,Seller_Type_Individual]])
        output=prediction
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
