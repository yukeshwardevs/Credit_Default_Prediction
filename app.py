from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Azure endpoint URL and authentication key
Endpoint = "https://credit-endpoint-1-64baceca.eastus.inference.ml.azure.com/score"
Auth_key = "mklqY8WbYbezmnFs2iwVMG9PpRI1c4on"

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('Index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect data from form
    data_row_1 = []
    data_row_2 = []

    for i in range(23):
        feature_value_row_1 = int(request.form.get(f'feature1_{i}'))
        feature_value_row_2 = int(request.form.get(f'feature2_{i}'))
        data_row_1.append(feature_value_row_1)
        data_row_2.append(feature_value_row_2)

    # Prepare data InputData for API
    InputData = {
        "input_data": {
            "columns": list(range(23)),
            "index": [0, 1],
            "data": [data_row_1, data_row_2]
        }
    }

    # Set headers with bearer token
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {Auth_key}'}

    try:
        # Make request to Azure endpoint
        response = requests.post(url=Endpoint, json=InputData, headers=headers)
        print("Response content:", response.content)  # Print response content for debugging

        # Process prediction result
        if response.status_code == 200:
            prediction = response.json()
            return render_template('Index.html', prediction=prediction)
        else:
            error_message = f"Error: {response.status_code}. Prediction failed."
            return render_template('Index.html', error_message=error_message)
    except Exception as e:
        error_message = str(e)
        return render_template('Index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
