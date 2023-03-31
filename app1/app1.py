from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from os.path import dirname, join
import joblib
import requests
import json
import numpy as np
import time
app1 = Flask(__name__)
CORS(app1)
current_dir = dirname(__file__)
model = joblib.load('./templates/model.pkl')
class DecodeJSON(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

class MakeApiCall:

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    def get_user_data(self, api, parameters):
        response = ''
        while response == '':
            try:
                response = requests.get(f"{api}", params=parameters)
                break
            except:
                time.sleep(2)
                continue
        if response.status_code == 200:
            # print("sucessfully fetched the data with parameters provided")
            res = self.formatted_print(response.json())
        else:
            res = "Hello person, there's a {response.status_code} error with your requests"
            # print(f"Hello person, there's a {response.status_code} error with your requests")
        return res
    
    def generatePredictions(self, f1, f2, f3, f4):
        # sc = pickle.load(open('./templates/scalerv2.pkl', 'rb'))
        sc = joblib.load('./templates/scaler.pkl')
        to_predict1 = sc.transform([f1])
        to_predict2 = sc.transform([f2])
        to_predict3 = sc.transform([f3])
        to_predict4 = sc.transform([f4])
        pred1 = model.predict(to_predict1)
        pred2 = model.predict(to_predict2)
        pred3 = model.predict(to_predict3)
        pred4 = model.predict(to_predict4)
        cnt1 = 0
        cnt2 = 0
        if(pred1[0] == 0):
            cnt1 += 1
        else:
            cnt2 += 1
        if(pred2[0] == 0):
            cnt1 += 1
        else:
            cnt2 += 1
        if(pred3[0] == 0):
            cnt1 += 1
        else:
            cnt2 += 1
        if(pred4[0] == 0):
            cnt1 += 1
        else:
            cnt2 += 1

        finalPred = cnt1 * 25
        majority = "Fertile"
        if(cnt1 > cnt2):
            majority = "Fertile"
        if(cnt1 == cnt2):
            majority = "Equal(50 - 50%)"
        if(cnt1 < cnt2):
            majority = "Infertile"

        return {'prediction[0 - 5cm]' : str(pred1[0]),
                'prediction[15 - 30cm]' : str(pred2[0]),
                'prediction[30 - 60cm]' : str(pred3[0]),
                'prediction[60 - 100cm]' : str(pred4[0]),
                'totalPrediction' : finalPred,
                'majority' : majority,
                'fertile_prediction_count' : cnt1,
                'infertile_prediction_count' : cnt2
                }

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        # print(text)
        dj = DecodeJSON(text) 
        #----------------CEC--------------------------------------
        cec1 = dj.properties["layers"][0]['depths'][0]['values']['mean'] / 10.0
        cec2 = dj.properties["layers"][0]['depths'][1]['values']['mean'] / 10.0
        cec3 = dj.properties["layers"][0]['depths'][2]['values']['mean'] / 10.0
        cec4 = dj.properties["layers"][0]['depths'][3]['values']['mean'] / 10.0
        #----------------Clay-------------------------------------
        clay1 = dj.properties["layers"][1]['depths'][0]['values']['mean'] / 10.0
        clay2 = dj.properties["layers"][1]['depths'][1]['values']['mean'] / 10.0
        clay3 = dj.properties["layers"][1]['depths'][2]['values']['mean'] / 10.0
        clay4 = dj.properties["layers"][1]['depths'][3]['values']['mean'] / 10.0
        #----------------nitrogen-----------------------------------
        nitrogen1 = dj.properties["layers"][2]['depths'][0]['values']['mean']
        nitrogen2 = dj.properties["layers"][2]['depths'][1]['values']['mean']
        nitrogen3 = dj.properties["layers"][2]['depths'][2]['values']['mean']
        nitrogen4 = dj.properties["layers"][2]['depths'][3]['values']['mean']
        #---------------ocd------------------------------------------
        ocd1 = dj.properties["layers"][3]['depths'][0]['values']['mean'] / 10.0
        ocd2 = dj.properties["layers"][3]['depths'][1]['values']['mean'] / 10.0
        ocd3 = dj.properties["layers"][3]['depths'][2]['values']['mean'] / 10.0
        ocd4 = dj.properties["layers"][3]['depths'][3]['values']['mean'] / 10.0
        #----------------pH--------------------------------------------------
        ph1 = dj.properties["layers"][4]['depths'][0]['values']['mean'] / 10.0
        ph2 = dj.properties["layers"][4]['depths'][1]['values']['mean'] / 10.0
        ph3 = dj.properties["layers"][4]['depths'][2]['values']['mean'] / 10.0
        ph4 = dj.properties["layers"][4]['depths'][3]['values']['mean'] / 10.0
        #---------------sand-------------------------------------------------
        sand1 = dj.properties["layers"][5]['depths'][0]['values']['mean'] / 10.0
        sand2 = dj.properties["layers"][5]['depths'][1]['values']['mean'] / 10.0
        sand3 = dj.properties["layers"][5]['depths'][2]['values']['mean'] / 10.0
        sand4 = dj.properties["layers"][5]['depths'][3]['values']['mean'] / 10.0
        #---------------silt---------------------------------------------------
        
        silt1 = dj.properties["layers"][6]['depths'][0]['values']['mean'] / 10.0
        silt2 = dj.properties["layers"][6]['depths'][1]['values']['mean'] / 10.0
        silt3 = dj.properties["layers"][6]['depths'][2]['values']['mean'] / 10.0
        silt4 = dj.properties["layers"][6]['depths'][3]['values']['mean'] / 10.0
        #---------------oc---------------------------------------------------
        oc1 = dj.properties["layers"][7]['depths'][0]['values']['mean'] / 10.0
        oc2 = dj.properties["layers"][7]['depths'][1]['values']['mean'] / 10.0
        oc3 = dj.properties["layers"][7]['depths'][2]['values']['mean'] / 10.0
        oc4 = dj.properties["layers"][7]['depths'][3]['values']['mean'] / 10.0

        #---------------make Predictions--------------------------------------
        features1 = [ph1, (oc1/1000.0), nitrogen1, (sand1/10.0), (silt1/10.0), (clay1/10.0), (cec1/10.0)]
        features2 = [ph2, (oc2/1000.0), nitrogen2, (sand2/10.0), (silt2/10.0), (clay2/10.0), (cec2/10.0)]
        features3 = [ph3, (oc3/1000.0), nitrogen3, (sand3/10.0), (silt3/10.0), (clay3/10.0), (cec3/10.0)]
        features4 = [ph4, (oc4/1000.0), nitrogen4, (sand4/10.0), (silt4/10.0), (clay4/10.0), (cec4/10.0)]
        pred = self.generatePredictions(features1, features2, features3, features4)
        
        return {
                    'cec':{
                        'cec[0 - 5cm]': cec1, 'cec[5 - 15cm]': cec2, 'cec[15 - 30cm]': cec3, 'cec[30 - 60cm]':cec4, 'unit' : 'cmol(c)/kg'
                    },
                    'clay': {
                        'clay[0 - 5cm]': clay1, 'clay[5 - 15cm]': clay2, 'clay[15 - 30cm]': clay3, 'clay[30 - 60cm]':clay4, 'unit': 'g/100g (%)'
                    },
                    'nitrogen' :{
                        'nitrogen[0 - 5cm]': nitrogen1, 'nitrogen[5 - 15cm]': nitrogen2, 'nitrogen[15 - 30cm]': nitrogen3, 'nitrogen[30 - 60cm]':nitrogen4, 'unit': 'g/kg'
                    },
                    'ph' : {
                        'ph[0 - 5cm]': ph1, 'ph[5 - 15cm]': ph2, 'ph[15 - 30cm]': ph3, 'ph[30 - 60cm]':ph4, 'unit': 'pH'
                    },
                    'sand' : {
                        'sand[0 - 5cm]': sand1, 'sand[5 - 15cm]': sand2, 'sand[15 - 30cm]': sand3, 'sand[30 - 60cm]':sand4, 'unit': 'g/100g(%)'
                    },
                    'silt' : {
                        'silt[0 - 5cm]': silt1, 'silt[5 - 15cm]': silt2, 'silt[15 - 30cm]': silt3, 'silt[30 - 60cm]':silt4, 'unit': 'g/100g (%)'
                    },
                    'oc' : {
                        'oc[0 - 5cm]': oc1, 'oc[5 - 15cm]': oc2, 'oc[15 - 30cm]': oc3, 'oc[30 - 60cm]':oc4, 'unit': 'g/kg'
                    },
                    'ocd' : {
                        'ocd[0 - 5cm]': ocd1, 'ocd[5 - 15cm]': ocd2, 'ocd[15 - 30cm]': ocd3, 'ocd[30 - 60cm]':ocd4, 'unit': 'kg/m³'
                    },
                    'predictions' : pred
                }


    def __init__(self, api):
        parameters = {
            "username": "kedark"
        }

class MakeCropRecommendation:
    lat = 0
    lon = 0
    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    def get_user_data(self, api, p):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            # print("sucessfully fetched the data with parameters provided")
            res = self.formatted_print(response.json(), p)
        else:
            res = "Hello person, there's a {response.status_code} error with your requests"
            # print(f"Hello person, there's a {response.status_code} error with your requests")
        return res
    
    
    def formatted_print(self, obj, p):
        text = json.dumps(obj, sort_keys=True, indent=4)
        # print(text)
        dj = DecodeJSON(text)
        r = 0
        
        for i in range(0,30):
            r = r + dj.forecast['forecastday'][i]['day']["totalprecip_mm"]
        humidity =  dj.forecast['forecastday'][0]['day']["avghumidity"]
        temperature =  dj.forecast['forecastday'][0]['day']["avgtemp_c"]
        rain = r
        ph1 = p['ph']["ph[0 - 5cm]"]
        ph2 = p['ph']["ph[5 - 15cm]"]
        ph3 = p['ph']["ph[15 - 30cm]"]
        ph4 = p['ph']["ph[30 - 60cm]"]
        n1 = p['nitrogen']["nitrogen[0 - 5cm]"]
        n2 = p['nitrogen']["nitrogen[5 - 15cm]"]
        n3 = p['nitrogen']["nitrogen[15 - 30cm]"]
        n4 = p['nitrogen']["nitrogen[30 - 60cm]"]

        crop_model = joblib.load('./templates/crop_model.pkl')
        crop_scaler = joblib.load('./templates/crop_scaler.pkl')

        f1 = [n1, temperature, humidity, ph1, rain]
        f2 = [n2, temperature, humidity, ph2, rain]
        f3 = [n3, temperature, humidity, ph3, rain]
        f4 = [n4, temperature, humidity, ph4, rain]
        print(f1)
        f1 = crop_scaler.transform([f1])
        f2 = crop_scaler.transform([f2])
        f3 = crop_scaler.transform([f3])
        f4 = crop_scaler.transform([f4])

        pred1 = crop_model.predict(f1)
        pred2 = crop_model.predict(f2)
        pred3 = crop_model.predict(f3)
        pred4 = crop_model.predict(f4)
        print(f1)
        return {
            "humidity" : humidity,
            "temperature" : temperature,
            "rain" : rain,
            "crop[0 - 5cm]" : pred1[0],
            "crop[5 - 15cm]" : pred2[0],
            "crop[15 - 30cm]" : pred3[0],
            "crop[30 - 60cm]" : pred4[0] 
        }

    def __init__(self, api):
        parameters = {
            "username": "kedark"
        }

@app1.route('/',methods=["GET","POST"])
def home():
    return "Agri11"

@app1.route('/post',methods=['POST'])
def predict():
    lat = str(request.args.get('Lat'))
    long = str(request.args.get('Long'))
    dt = str(request.args.get('date'))
    end_dt = str(request.args.get('end_dt'))
    api_call = MakeApiCall("https://rest.isric.org/soilgrids/v2.0/properties/query")
    parameters = {
                "lon" : long, 
                "lat": lat,
                "property" : [ "cec", "clay", "nitrogen", "phh2o", "sand", "silt", "soc", 'ocd'],
                "depth" : ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm"],
                "value" : ['mean', 'uncertainty']
            }
    res = api_call.get_user_data("https://rest.isric.org/soilgrids/v2.0/properties/query", parameters)
    #url = "http://api.weatherapi.com/v1/history.json?key=9d99901a21c54149a7d72015231902&q={},{}&dt={}&hour=15&end_dt={}".format(lat,long,dt,end_dt)
    #api_call1 = MakeCropRecommendation("https://rest.isric.org/soilgrids/v2.0/properties/query")
    #crop = api_call1.get_user_data(url, res)
    pred = {'Server': ["Server 1"],'Parameters' : [lat, long, dt, end_dt],'Fertility' : res, 'crop' : "Not Available"}
    return jsonify(pred)

if __name__ == "__main__":
    app1.run(debug=True)
