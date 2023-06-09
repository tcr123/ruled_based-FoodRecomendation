from flask import Flask, request, jsonify
import pandas as pd
import pickle
from kbase.patient import Patient
import kbase.rules as rules

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Testing really work?'

@app.route('/about', methods=['GET'])
def about():
    return 'About'

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Load the .pkl file
#     with open('model/content_based_model.pkl', 'rb') as file:
#         model = pickle.load(file)

#     food_dataset = pd.read_csv('dataset/data_eng.csv')
#     nutrient_dummies = food_dataset.Nutrient.str.get_dummies()
#     disease_dummies = food_dataset.Disease.str.get_dummies(sep=' ')
#     diet_dummies = food_dataset.Diet.str.get_dummies(sep=' ')
#     feature_df = pd.concat([nutrient_dummies,disease_dummies,diet_dummies],axis=1)

#     total_features = feature_df.columns
#     d = dict()
#     for i in total_features:
#         d[i]= 0
    
#     # Get the data from the POST request
#     data = request.get_json()
#     if data is not None and 'data' in data and isinstance(data['data'], list):
#         features = data['data']
#         for feature in features:
#             d[feature] = 1
    
#     final_input = list(d.values())
#     # print(final_input)

#     distances, indices = model.kneighbors([final_input])

#     results = []

#     for i in indices.flatten():
#         meal_id = food_dataset.loc[i]['Meal_Id']
#         results.append(meal_id)
    
#     response = jsonify(results)

#     return response

@app.route('/predict', methods=['POST'])
def diet():

    # Load the .pkl file
    with open('model/content_based_model.pkl', 'rb') as file:
        model = pickle.load(file)

    food_dataset = pd.read_csv('dataset/data_eng.csv')
    nutrient_dummies = food_dataset.Nutrient.str.get_dummies()
    disease_dummies = food_dataset.Disease.str.get_dummies(sep=' ')
    diet_dummies = food_dataset.Diet.str.get_dummies(sep=' ')
    feature_df = pd.concat([nutrient_dummies,disease_dummies,diet_dummies],axis=1)

    total_features = feature_df.columns
    d = dict()
    for i in total_features:
        d[i]= 0

    # Get the data from the POST request
    data = request.get_json()
    if data is not None and 'data' in data and isinstance(data['data'], dict):
        patient_data = data['data']
        patient = Patient(patient_data)

        # features = rules.get_features(patient)

        # for feature in features:
        #     if feature in total_features:
        #         d[feature] = 1

        # final_input = list(d.values())

        # print(final_input)

        # indices = model.kneighbors([final_input], return_distance=False)

        # results = []

        # for i in indices.flatten():
        #     meal_id = food_dataset.loc[i]['Meal_Id']
        #     results.append(meal_id)

        # results = list(set(results))

        ''''''
        # results = rules.get_meals(patient)

        diagnosis_results = rules.evaluate_all_rules(patient)

        high_risk_diseases = [k for k, v in diagnosis_results.items() if v]

        recommended_diet = []
        for disease, present in diagnosis_results.items():
            if present:
                recommended_diet += food_dataset[food_dataset['Disease'].str.contains(disease)]['Meal_Id'].tolist()

        # remove duplicates
        results = list(set(recommended_diet))

        response = jsonify({
            "meal_ids": results,
            "diagnosis": high_risk_diseases,
        })
    else:
        response = jsonify('Invalid request')
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
