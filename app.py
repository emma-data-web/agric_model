from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the pickled preprocessor and model
with open('preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Health check route (optional)
@app.route('/show', methods=['GET'])
def show():
    return 'nuelsah is here!'

# Web form route
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            # Extract features from the form
            soil_ph = float(request.form.get("soil_ph"))
            soil_moisture = float(request.form.get("soil_moisture"))
            temperature = float(request.form.get("temperature"))
            rainfall = float(request.form.get("rainfall"))
            crop_type = request.form.get("crop_type")
            fertilizer = float(request.form.get("fertilizer"))
            pesticide = float(request.form.get("pesticide"))
            Crop_Yield_ton = float(request.form.get("Crop_Yield_ton"))
            
            # Prepare input data
            input_data = pd.DataFrame([[
                soil_ph, soil_moisture, temperature, rainfall,
                crop_type, fertilizer, pesticide, Crop_Yield_ton
            ]], columns=[
                'Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm',
                'Crop_Type', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg','Crop_Yield_ton'
            ])

            # Transform and predict
            X = preprocessor.transform(input_data)
            result = model.predict(X)[0]
            prediction = f"Estimated sustainability: {result:.2f} units"

        except Exception as e:
            prediction = f"Error: {str(e)}"
    
    return render_template("index.html", prediction=prediction)

# API route for JSON input
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        input_data = pd.DataFrame([data], columns=[
            'Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm',
            'Crop_Type', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg','Crop_Yield_ton'
        ])

        input_processed = preprocessor.transform(input_data)
        prediction = model.predict(input_processed)

        return jsonify({'prediction': float(prediction[0])})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)