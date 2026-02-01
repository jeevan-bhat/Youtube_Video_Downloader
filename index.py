import requests
from flask import Flask,request,render_template











app = Flask(__name__)

API_KEY="YOUR_API_KEY"
BASE_URL="https://api.openweathermap.org/data/2.5/weather"
# city=input("Enter the city name : ")





@app.route('/',methods=["GET","POST"])
def index():
    weather_data = None
    error = None
    if request.method=="POST":
        city=request.form['city']
        params = {
        "q": city,
        "appid": "API_KEY",
        "units": "metric"
    }





        response=requests.get(BASE_URL,params=params)


        if response.status_code ==200:
            x=response.json()
            weather_data={
                "city": city,
                "temperature": x["main"]["temp"],
                "humidity": x["main"]["humidity"],
                "condition": x["weather"][0]["description"],
                "wind": x["wind"]["speed"]
            }

        else:
            print("city not found:")


    return render_template('index.html',weather=weather_data, error=error)


if __name__ == '__main__':
    app.run(debug=True)

























# print(x)