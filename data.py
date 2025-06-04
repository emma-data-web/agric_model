import requests

url = 'http://127.0.0.1:5000/predict'
data = {
   'Soil_pH': 6.8,
    'Soil_Moisture': 28,
    'Temperature_C': 22,
    'Rainfall_mm': 150,
    'Crop_Type': 'Wheat',  # match case exactly
    'Fertilizer_Usage_kg': 100,
    'Pesticide_Usage_kg': 5,
    'Crop_Yield_ton': 8
}


response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response text:", response.text)

