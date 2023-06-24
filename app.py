# from flask import Flask, render_template, request
# import joblib
# import pandas as pd

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def predict():
#     print("hei")
#     if request.method == 'POST':
#         print("hello")
#         # Încarcă caracteristicile introduse de utilizator într-un DataFrame
#         rooms=int(request.form.get('rooms'))
#         surface_area = float(request.form.get('surface_area'))
#         num_bathrooms = int(request.form.get('num_bathrooms'))
#         num_balconies = int(request.form.get('num_balconies'))
#         floor = int(request.form.get('floor'))
#         parking_spaces = int(request.form.get('parking_spaces'))
#         basement_storage = int(request.form.get('basement_storage'))
#         neighborhood = float(request.form.get('neighborhood'))
#         building_years = int(request.form.get('building_years'))

#         data = {
#             'Nr. camere':[rooms],
#             'Suprafață utilă': [surface_area],
#             'Nr. băi': [num_bathrooms],
#             'Nr. balcoane': [num_balconies],
#             'Etaj': [floor],
#             'Locuri de parcare': [parking_spaces],
#             'Boxă la subsol': [basement_storage],
#             'Cartier': [neighborhood],
#             'building_years': [building_years]
#         }
#         user_input = pd.DataFrame(data)
#         print(data)
#         print(user_input)

#         # Încarcă modelul antrenat din fișierul .pkl
#         model = joblib.load('model.pkl')

#         print(model)
#         coefficients = model.coef_

#         print(coefficients)
#         # Verifică dimensiunea coeficienților
        

#         # Calculează prețul total estimat
#         price = sum(coefficients[1:9] * user_input.values.flatten()[1:9])
#         price_total = price

#         return render_template('index.html', price=price_total)
#     else:
#         return render_template('index.html', price =0)

# if __name__ == '__main__':
#     app.run()

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from openpyxl import Workbook
from bs4 import BeautifulSoup
import re




app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        rooms = int(request.json.get('rooms'))
        surface_area = float(request.json.get('surface_area'))
        num_bathrooms = int(request.json.get('num_bathrooms'))
        num_balconies = int(request.json.get('num_balconies'))
        floor = int(request.json.get('floor'))
        parking_spaces = int(request.json.get('parking_spaces'))
        basement_storage = int(request.json.get('basement_storage'))
        neighborhood = float(request.json.get('neighborhood'))
        building_years = int(request.json.get('building_years'))

        data = {
            'Nr. camere': [rooms],
            'Suprafață utilă': [surface_area],
            'Nr. băi': [num_bathrooms],
            'Nr. balcoane': [num_balconies],
            'Etaj': [floor],
            'Locuri de parcare': [parking_spaces],
            'Boxă la subsol': [basement_storage],
            'building_years': [building_years],
            'Cartier': [neighborhood],
        }
        user_input = pd.DataFrame(data)

        model = joblib.load('model.pkl')
        coefficients = model.coef_
        print(coefficients[1:9])
        print(user_input.values.flatten()[1:9])
        price = sum(coefficients[1:10] * user_input.values.flatten()[0:9])

        return jsonify({'price': price})
    else:
        return jsonify({'price': 0})

@app.route('/extract', methods=['GET'])
def extract_data():
    # Codul de extragere a datelor
    anunturi = []
    existing_data = pd.read_excel('output.xlsx')
    recent_date = existing_data['Data anunt'].max()
    
    PATH = "C:\\Users\\Larisa\\Desktop\\licenta\\chromedriver2"
    driver = webdriver.Chrome(PATH)
    
    url = "https://www.blitz.ro/cluj-napoca/vanzari-apartamente"
    driver.get(url)
    
    count = 0
    cards = driver.find_elements(By.CSS_SELECTOR, '.card')
    for i in range(len(driver.find_elements(By.CSS_SELECTOR, '.card__content'))):
        try:
            if count == 90:
                break
            
            card = driver.find_elements(By.CSS_SELECTOR, '.card__content')[i]
            link = card.find_element(By.CSS_SELECTOR, '.card__content--head a').get_attribute('href')
            print(link)
            driver.get(link)
            
            offer_features = driver.find_element(By.CSS_SELECTOR, '.offer-features')
            soup = BeautifulSoup(offer_features.get_attribute('innerHTML'), 'html.parser')
            
            offer_info = driver.find_element(By.CSS_SELECTOR, '.offer-informations')
            soup2 = BeautifulSoup(offer_info.get_attribute('innerHTML'), 'html.parser')
            
            anunt = {}
    
            for strong in soup.find_all('strong'):
                column_name = strong.text.strip()
                anunt[column_name] = ''
    
            if offer_info is not None:
                for item in soup2.find_all('div', class_='offer-informations--item'):
                    strong_tags = item.find_all('strong')
                    if strong_tags is not None:
                        for index, strong_tag in enumerate(strong_tags):
                            if 'Cartier : ' in strong_tag.text:
                                column_value = ''
                                if strong_tag.next_sibling is not None:
                                    column_value = strong_tag.next_sibling.strip()
                                    print(column_value)
                                    anunt['Cartier'] = column_value
                            elif 'Pret/mp: ' in strong_tag.text:
                                column_value = ''
                                if strong_tag.next_sibling is not None:
                                    column_value = strong_tag.next_sibling.strip()
                                    numeric_value = re.search(r'\d+[\.,]?\d*', column_value)
                                    if numeric_value:
                                        column_value = numeric_value.group(0).replace('.', '')
                                        column_value = column_value.replace(',', '.')
                                    print(column_value)
                                    anunt['Pret/mp'] = column_value 
                            elif 'Actualizat:' in strong_tag.text:
                                column_value = ''
                                if strong_tag.next_sibling is not None:
                                    column_value = strong_tag.next_sibling.strip()
                                    anunt['Data anunt'] = column_value  
                                    
            for li in soup.find_all('li'):
                for strong in li.find_all('strong'):
                    column_name = strong.text.strip()
                    column_value = ''
                    if strong.next_sibling is not None:
                        column_value = strong.next_sibling.strip()
                    numeric_value = re.search(r'\d+[\.,]?\d*', column_value)
                    if numeric_value:
                        column_value = numeric_value.group(0).replace(',', '.')
                        print(column_value)    
                    anunt[column_name] = column_value
    
            print(anunt) 
            if pd.to_datetime(anunt['Data anunt']) > pd.to_datetime(recent_date):
                anunturi.append(anunt)
                
            driver.back()
        except NoSuchElementException:
            continue
        count += 1 
        
    df2 = pd.DataFrame(anunturi)
    new_data = pd.DataFrame(anunturi)
    df_final = pd.concat([existing_data, new_data], ignore_index=True)
    print(df_final)
    df_final.to_excel('output.xlsx', index=False)
    
    driver.quit()
    
    return jsonify({'message': 'Extraction completed', 'num_data': len(anunturi)})    
    

if __name__ == '__main__':
    app.run()
