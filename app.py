from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

#  the pickled preprocessor and model
with open('preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/show', methods=['GET'])
def show():
    return 'nuelsah is here!'


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    columns = [
        'Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm',
        'Crop_Type', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg', 'Crop_Yield_ton'
    ]

    # Convert input JSON to DataFrame
    

    # Preprocess  features

    
    try:
        # Build input dataframe
        
        input_df = pd.DataFrame([data], columns=columns)

        # Transform input using the preprocessor
        input_processed = preprocessor.transform(input_df)

        # Make prediction
        prediction = model.predict(input_processed)

        # Return result
        return jsonify({'prediction': (prediction[0])})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)