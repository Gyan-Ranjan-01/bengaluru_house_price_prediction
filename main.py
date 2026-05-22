from flask import Flask, request, render_template, jsonify
import pandas as pd
import pickle
import json

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
    )

#loading the model
with open("House_Predicting_Model.pickle",'rb') as f:
    model=pickle.load(f)

#reading file
df = pd.read_csv("Bengaluru_House_Data.csv")
df.dropna(subset=['location'],inplace=True)
df['location'] = df['location'].astype(str)
df = df[df.groupby('location')['location'].transform('count') > 10]
locations = sorted(df['location'].unique())

@app.route('/')
def home():
    return render_template('index.html',locations=locations)

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = pd.DataFrame([{
            'location': data['location'],
            'total_sqft': float(data['total_sqft']),
            'bath': float(data['bath']),
            'balcony': float(data['balcony']),
            'bhk': float(data['bhk'])
        }])
        prediction = model.predict(input_data)[0]
        return jsonify({'success': True, 'predicted_price': round(prediction, 2)})

    except Exception as e:
        return jsonify({'success': False, 'err' : str(e)}),400

# if __name__=="__main__":
#     app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)