import requests
import json

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
        response = requests.post(f"{api}", params=parameters)
        print(parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
        # dj = DecodeJSON(text) 
        # print(dj.properties["layers"][0]['depths'][0])
        # print(dj.properties["layers"][0]['depths'][1])
        # print(dj.properties["layers"][0]['depths'][2])
        # print(dj.properties["layers"][0]['depths'][3])

    def __init__(self, api):
        parameters = {
            "username": "kedark"
        }


if __name__ == "__main__":
    # lat = input("Enter Latitude: ")
    # long = input("Enter Longititude: ")

    parameters = {
            "Lat" : "19.704656",
            "Long" : "74.248489",
            "date" : "2022-07-01",
            "end_dt" : "2022-07-30"
        }
    appid='1e6404a478eb82a222f938c29dd8a262'
    lat= "15.203628"
    lon= "74.513289"
    api_call = MakeApiCall("http://127.0.0.1:5000")
    #api_call.get_data("http://api.weatherapi.com/v1/history.json?key=c6520399656c4760937143836221711&q={lat},{lon}&dt=2022-07-01&hour=15")
    #print("http://api.weatherapi.com/v1/history.json?key=c6520399656c4760937143836221711&q={lat},{lon}&dt=2022-07-01&hour=15")
    #api_call.get_user_data("https://soil-health.herokuapp.com/post", parameters)
    api_call.get_user_data("http://127.0.0.1:5000/post", parameters)
