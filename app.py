import requests #this module will allow you to send HTTP/1.1 requests
import configparser #this module will allow to parse the config file and we made the config file because we shouldn't really hardcode anything in the main app file.
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def weather_results():
    zip_code = request.form['zipCode']    
    api_key = get_api_key()
    data = weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    return render_template('results.html', location = location, temp = temp, feels_like = feels_like, weather = weather)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['WeatherReportApp']['api'] #returns the apikey

def weather_results(zip_code, api_key): #function will take in zip code and api key and return the results for calling the api
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key) #format basically puts in the paramters entered by the user into the empty curly braces
    returned_request = requests.get(api_url) #a function of the requests module
    return returned_request.json() #converts the data into a json format
    
if __name__ == '__main__': #ensures that app only runs once and multiple instances aren't created 
    app.run()

