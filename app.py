import asyncio
import aiohttp
from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
api = Api(app)

data_file = 'data/weather_data.json'

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

class WeatherCollector(Resource):
    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_API_KEY")
        self.weather_data = load_data()

    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        city_ids = data['city_ids']

        if user_id in self.weather_data:
            return {"message": "User ID already exists"}, 400

        self.weather_data[user_id] = {
            "datetime": datetime.now().isoformat(),
            "progress": 0,
            "data": []
        }
        save_data(self.weather_data)

        asyncio.run(self.collect_weather_data(user_id, city_ids))
        return {"message": "Data collection in progress"}, 202

    async def collect_weather_data(self, user_id, city_ids):
        async with aiohttp.ClientSession() as session:
            total_cities = len(city_ids)
            tasks = []
            for idx, city_id in enumerate(city_ids):
                if idx % 60 == 0 and idx != 0:
                    await asyncio.sleep(60)
                tasks.append(self.fetch_weather(session, user_id, city_id, city_ids))
                if len(tasks) >= 60:
                    await asyncio.gather(*tasks)
                    tasks = []
            if tasks:
                await asyncio.gather(*tasks)
            
            self.weather_data[user_id]["progress"] = 100
            save_data(self.weather_data)

    async def fetch_weather(self, session, user_id, city_id, city_ids):
        async with session.get(f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={self.api_key}&units=metric") as response:
            data = await response.json()
            if 'main' in data:
                self.weather_data[user_id]["data"].append({
                    "city_id": city_id,
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"]
                })
                progress = len(self.weather_data[user_id]["data"]) / len(city_ids) * 100
                self.weather_data[user_id]["progress"] = progress
                save_data(self.weather_data)

class Progress(Resource):
    def get(self, user_id):
        if user_id in load_data():
            return jsonify(load_data()[user_id])
        else:
            return {"message": "User not found"}, 404

api.add_resource(WeatherCollector, '/collect')
api.add_resource(Progress, '/progress/<string:user_id>')

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(host='0.0.0.0', port=5000, debug=False)