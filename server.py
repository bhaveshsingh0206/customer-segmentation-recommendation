import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno
import pickle
import sys

import json
from sklearn.preprocessing import LabelEncoder, OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
import keras
import tensorflow as tf
from joblib import dump,load
from flask_cors import CORS
keras.backend.clear_session()

global graph
graph = tf.get_default_graph()

classifier_predict_score = keras.models.load_model('models/classifier_predict_score.h5')
classifier_predict_camera_lover = keras.models.load_model('models/classifier_predict_camera_lover.h5')
classifier = keras.models.load_model('models/classifier.h5')
classifier_predict_user = keras.models.load_model('models/classifier_predict_user.h5')

classifier_predict_brand_lover = keras.models.load_model('models/classifier_predict_brand_lover.h5')


df=pd.read_csv('datasets/Dataset.csv')


def create_demographics(df):
    demographics=pd.DataFrame(df.groupby(['City','State','Country'])['Brand'].value_counts())
    demographics.rename(columns={'Brand':'Count'},inplace=True)
    demographics=demographics.reset_index()
    demographics['Brand_Recommend']='Recommend Popular'
    demographics['Brand_Recommend'].loc[demographics['Count']>=2]=demographics['Brand'].loc[demographics['Count']>=2]
    demographics=pd.DataFrame(demographics.groupby(['City','State'])['Brand'].unique()).reset_index()
    demographics.rename(columns={'Brand':'Recommend'},inplace=True)
    demographics['Recommend']=demographics['Recommend'].astype(str)
    demographics['Recommend']=demographics['Recommend'].str.strip('[]')
    return demographics

demographics=create_demographics(df)
# demographics

# Visualizing types of customers on the basis of Entuitive Score
def visualizing_user(df,status): 
    classisfying_user = pd.DataFrame(df.groupby('ID')['Score'].mean())
    classisfying_user.reset_index(inplace=True)
    classisfying_user['category'] = np.nan
    j = 0
    for row in classisfying_user.itertuples():
        if row.Score > 500 : 
            classisfying_user['category'][j] = 'Luxurious'
        elif row.Score > 375 : 
            classisfying_user['category'][j] = 'Tech Savvy'
        elif row.Score > 250 : 
            classisfying_user['category'][j] = 'Flagship Killers'
        elif row.Score > 125 : 
            classisfying_user['category'][j] = 'Reasonable Brand Seekers'
        else : 
            classisfying_user['category'][j] = 'Budget Oriented'
        j += 1
    if status :
        fig = plt.figure(figsize=(20, 5))
        sns.countplot(data=classisfying_user, x='category')
    return classisfying_user

x=visualizing_user(df, False)
classisfying_user = x
# Processing Data to identify Brand Lover in our dataset
def Brand_lover(df):
    brand_lover = pd.DataFrame(df.groupby(['ID','Brand'])['Model'].count()).reset_index()
    brand_lover.rename(columns={'Model':'Brandwise_Count'},inplace=True)
    temp=pd.DataFrame(df.groupby('ID')['Model'].count()).reset_index()
    temp.rename(columns={'Model':'Total_Purchases'},inplace=True)
    brand_lover=brand_lover.merge(temp)    
    columns = df.Brand.unique()
    
    for col in columns:
        brand_lover[col] = np.nan
        
    i = 0
    for row in brand_lover.itertuples():
        x = (row.Brandwise_Count / row.Total_Purchases)
        brand_lover[row.Brand][i] = x
        i+=1
        
    brand_lover=brand_lover.fillna(0)
    temp=brand_lover.groupby(['ID'])[['Apple','Samsung','Motorola','Alcatel','Sony','LG','ZTE','Huawei','HTC','Windows','BLU','Google']].sum()
    brand_lover=brand_lover.drop(columns=['Apple','Samsung','Motorola','Alcatel','Sony','LG','ZTE','Huawei','HTC','Windows','BLU','Google'])    
    brand_lover=brand_lover.drop_duplicates(subset="ID",keep='first')    
    temp=temp.reset_index()
    brand_lover=brand_lover.merge(temp)
    
    brand_lover['Category'] = np.nan
    brand_lover['Confidence'] = np.nan
    i=0
    for row in brand_lover.itertuples():
        p = 'ID=='+str(row.ID)
        x=brand_lover.query(p)
        t=x[['Apple','Samsung','Motorola','Alcatel','Sony','LG','ZTE','Huawei','HTC','Windows','Google','BLU']].apply(lambda x:x.argmax(),axis=1)
        t=pd.DataFrame(t).reset_index()
        maxi = t[0].to_string().split(' ')[4]
        if brand_lover[maxi][i] > 0.6:
            brand_lover['Category'][i] = maxi + ' Lover'
            brand_lover['Confidence'][i] = brand_lover[maxi][i]
        else :
            brand_lover['Category'][i] = 'Sensible'
            brand_lover['Confidence'][i] = 0
        i+=1
        brand_lover['Category'] = np.where(brand_lover['Total_Purchases']<=2,'Sensible',brand_lover['Category'])
        brand_lover['Confidence'] = np.where(brand_lover['Total_Purchases']<=2,0,brand_lover['Confidence'])

    
    return brand_lover
 
#brand_lover=Brand_lover(df)    

def Camera_Lovers(df):
    camera_lover=df[['ID','Front Camera','Rear Camera']]
    camera_lover['Camera']=(camera_lover['Front Camera']*camera_lover['Rear Camera'])/(camera_lover['Front Camera'].max()*camera_lover['Rear Camera'].max())
    camera_lover['Type']='Sensible'
    camera_lover['Type'].loc[camera_lover['Camera']>=0.15]='Photophile'
    camera_lover['Type'].loc[camera_lover['Front Camera']>=25]='Selfie-Addict'
    camera_lover.rename(columns={'Camera':'Confidence'},inplace=True)
    camera_lover=camera_lover.sort_values(by='Confidence',ascending=False)
    camera_lover=camera_lover.drop_duplicates(subset='ID',keep='first')
    
    return camera_lover

camera_lover=Camera_Lovers(df) 

def convert_days(df):
    df['current'] = pd.to_datetime('now')
    arr=['Transaction_date','Account_Created', 'Last_Login']
    for i in arr:
        df[i] = pd.to_datetime(df[i])
        df[i] = df['current'].sub(df[i]) 
        df[i] = df[i] / np.timedelta64(1,'D')
        df[i] = df[i].round(0)

convert_days(df)  

def Customer_last_purchase(df):
    last_purchase=df
    last_purchase['current'] = pd.to_datetime('now')
    last_purchase['Transaction_date'] = pd.to_datetime(last_purchase['Transaction_date'])
    last_purchase['Transaction_date'] = last_purchase['current'].sub(last_purchase['Transaction_date']) 
    last_purchase['Transaction_date'] = last_purchase['Transaction_date'] / np.timedelta64(1,'D')
    last_purchase['Transaction_date'] = last_purchase['Transaction_date'].round(0)
    last_purchase=last_purchase[['Transaction_date','ID','Score']]
    last_purchase=last_purchase.sort_values(by=['ID','Transaction_date']).reset_index(drop=True)
    last_purchase=last_purchase.drop_duplicates(subset=['ID'],keep='first')
    last_purchase=last_purchase.reset_index(drop=True)
    return last_purchase

last_purchase=Customer_last_purchase(df)  

def Offers_Customer(df):
    Offers=df[['ID','Count','Account_Created','Transaction_date']]
    Offers['Type']='Intermediate Customer'
    Offers['Type'].loc[Offers['Count']>3 ]='Regular Customer'
    Offers=Offers.drop_duplicates(subset="ID",keep='first')
    return Offers

Offers=Offers_Customer(df)




predict_model_for_city = create_demographics(df)

predict_model_for_city_X = predict_model_for_city.iloc[:,:-1].values
predict_model_for_city_y = predict_model_for_city.iloc[:,2].values
    
label_encoder_x1 = LabelEncoder()
label_encoder_x2 = LabelEncoder()
    
predict_model_for_city_X[:,0] = label_encoder_x1.fit_transform(predict_model_for_city_X[:,0])
predict_model_for_city_X[:,1] = label_encoder_x2.fit_transform(predict_model_for_city_X[:,1])
    
onehotencoder_x1 = OneHotEncoder(categorical_features=[0,1])
predict_model_for_city_X = onehotencoder_x1.fit_transform(predict_model_for_city_X).toarray()
label_encoder_y = LabelEncoder()
predict_model_for_city_y[:] = label_encoder_y.fit_transform(predict_model_for_city_y[:])
predict_model_for_city_y = predict_model_for_city_y.reshape(766,1)

X_train = predict_model_for_city_X[:,1:]
X_train = X_train[:,0:-1]
    






def predict_city(city, state):
    X = [[city],[state]]
    X[0] = label_encoder_x1.transform(X[0])
    X[1] = label_encoder_x2.transform(X[1])
    predict_X = onehotencoder_x1.transform([[X[0][0],X[1][0]]]).toarray()
    predict_X = predict_X[:,1:]
    predict_X = predict_X[:,0:-1]
    predictions = classifier.predict(predict_X)
    classes = np.argmax(predictions, axis=1)
    return (label_encoder_y.inverse_transform([classes[0]])[0])

# print(predict_city('Aberdeen', 'Scotland'))
#Model2 Training and Testing
#Getting Category of User on basis of Antutu Score
get_category_of_user=visualizing_user(df, False)
get_category_of_user=get_category_of_user.drop(columns=['ID'])
get_category_of_user_X = get_category_of_user.iloc[:,:-1].values
get_category_of_user_y = get_category_of_user.iloc[:,1:2].values

labelencoder_get_category_of_user_y = LabelEncoder()
get_category_of_user_y = labelencoder_get_category_of_user_y.fit_transform(get_category_of_user_y)

sc_get_category_of_user_X = StandardScaler()
get_category_of_user_X = sc_get_category_of_user_X.fit_transform(get_category_of_user_X)

predict_score_X_train, predict_score_X_test, predict_score_y_train, predict_score_y_test = train_test_split(get_category_of_user_X, get_category_of_user_y, test_size = 0.2, random_state = 0)



def predict_user(score):
    X = [[score]]
    X = sc_get_category_of_user_X.transform(X)
    with graph.as_default():
    	predictions = classifier_predict_user.predict(X)
    classes = np.argmax(predictions, axis=1)
    return labelencoder_get_category_of_user_y.inverse_transform([classes[0]])[0]

# print(predict_user(502))


#Model3 Training and Testing
#Predicting Camera Lovers

predict_camera_lover=camera_lover=Camera_Lovers(df)
predict_camera_lover=predict_camera_lover.drop(columns=['ID'])


predict_camera_lover_X = predict_camera_lover.iloc[:,:-1].values
predict_camera_lover_y = predict_camera_lover.iloc[:,3:4].values
predict_camera_lover_X
labelencoder_predict_camera_lover_y = LabelEncoder()
predict_camera_lover_y = labelencoder_predict_camera_lover_y.fit_transform(predict_camera_lover_y)

sc_predict_camera_lover_X = StandardScaler()
predict_camera_lover_X = sc_predict_camera_lover_X.fit_transform(predict_camera_lover_X)




def predict_camera(front_camera, rear_camera):
    
    confidence = (front_camera*rear_camera)/(predict_camera_lover['Front Camera'].max()*predict_camera_lover['Rear Camera'].max())
    X = [[front_camera,rear_camera,confidence]]

    X = sc_predict_camera_lover_X.transform(X)
    with graph.as_default():
    	predictions = classifier_predict_camera_lover.predict(X)
    classes = np.argmax(predictions, axis=1)
    return labelencoder_predict_camera_lover_y.inverse_transform([classes[0]])[0]
# print(predict_camera(30, 30))


#Model4 Training and Testing
#Predicting antutu score on the basis of processor,ram,storage,battery,score

def Antutu_Score(df):
    predict_score=df[['Processor','RAM','Storage','Battery','Score']]
    predict_score = predict_score.loc[:,~predict_score.columns.duplicated()]
    predict_score=predict_score.drop_duplicates(keep='first')
    return predict_score

antutu_score=Antutu_Score(df)
# antutu_score

predict_score=Antutu_Score(df)
predict_score_X = predict_score.iloc[:,0:-1].values
predict_score_y = predict_score.iloc[:,4:5].values
labelencoder_predict_score_X = LabelEncoder()
predict_score_X[:,0] = labelencoder_predict_score_X.fit_transform(predict_score_X[:,0])
onehotencoder_predict_score_X = OneHotEncoder(categorical_features=[0])
predict_score_X = onehotencoder_predict_score_X.fit_transform(predict_score_X).toarray()
predict_score_X = predict_score_X[:,1:]
sc_predict_score_X = StandardScaler()
sc_predict_score_y = StandardScaler()
predict_score_X = sc_predict_score_X.fit_transform(predict_score_X)
predict_score_y = sc_predict_score_y.fit_transform(predict_score_y)
predict_score_X_train, predict_score_X_test, predict_score_y_train, predict_score_y_test = train_test_split(predict_score_X, predict_score_y, test_size = 0.0001, random_state = 0)



 
def predict_antutu_score(processor, ram, storage, battery):
    X = [[processor],[ram],[storage],[battery]]
    X[0] = labelencoder_predict_score_X.transform(X[0])
    predict_X = onehotencoder_predict_score_X.transform([[X[0][0],X[1][0],X[2][0],X[3][0]]]).toarray()
    predict_X = predict_X[:,1:]
    predict_X = sc_predict_score_X.transform(predict_X)
    with graph.as_default():
    	predictions = classifier_predict_score.predict(predict_X)
    predicted_score = sc_predict_score_y.inverse_transform(predictions)
    predicted_score = predicted_score[0][0]
    return predicted_score



#Model5 Training and Testing
#Predicting wherther user is a brand lover or not

class style:
    BOLD = '\033[1m'
    END = '\033[0m'
def predict_category_of_users_who_can_buy(brand, processor, front_camera, rear_camera, ram, storage, battery):
    score = predict_antutu_score(processor, ram, storage, battery)
    score = sc_predict_score_y.inverse_transform(score)
    print('=====================================================================')
    print('The predicted benchmark score of the mobile is '+style.BOLD+str(score[0][0])+style.END)
    print('=====================================================================')
    print('This particular mobile can be give as a recommendation to the following users')
    print(style.BOLD+'1. Based on the score with the score based categories of existing user'+style.END)
    print(str(predict_user(score[0][0])))
    print(style.BOLD+'2. Based on the Camera Specs which category of user will prefer'+style.END)
    camera_specs = predict_camera(front_camera, rear_camera)
    if camera_specs == "'Sensible'":
        print('Camera is avg hence it is not bought by camera lovers')
    else:
        print(camera_specs)
    if brand == 'Apple' or 'Samsung' or 'LG':
        print(style.BOLD+'3. Most Likely this mobile can be bought by people who are:'+style.END)
        print(brand+' Lovers')
    else:
        print(style.BOLD+'3. No Specific Brand Interest'+style.END)

# predict_category_of_users_who_can_buy('Apple', 'Apple A13 Bionic', 12, 24, 6, 128, 3000)
print("####################################################")

#Model6 Training and Testing
#Predicting Brand LOver  for Users

predict_brand=pd.read_csv('datasets/Brand_Lover.csv')
#predict_brand=Brand_lover(df)
predict_brand=predict_brand.drop(columns=['ID'])
#predict_brand.drop(['Brand','Brandwise_Count'], axis=1, inplace=True)
predict_brand_y = predict_brand.iloc[:,13:14].values
predict_brand_X = predict_brand.drop(['Apple','Category'], axis=1).iloc[:,:-1].values
labelenocer_predict_brand_y = LabelEncoder()
predict_brand_y = labelenocer_predict_brand_y.fit_transform(predict_brand_y)
sc_predict_brand_X = StandardScaler()
predict_brand_X = sc_predict_brand_X.fit_transform(predict_brand_X)


Brand_Lover = pd.read_csv('datasets/Brand_Lover.csv')
Camera_Lover = pd.read_csv('datasets/Camera_Lover.csv')
temp = df.merge(classisfying_user)
temp_camera = df.merge(Camera_Lover)
def predict_mobile_for_users(ID):
    print("i m here")
    brand=pd.DataFrame(Brand_Lover.query('ID=='+str(ID))['Category']).reset_index(drop=True)
    brand = list(brand.Category)[0]
    print(style.BOLD+'1. Based on Mobile brands!!'+style.END)
    if brand != 'Sensible':
    	rec_brand = "The above person is a <strong>"+brand+"</strong>. Hence Recommending him those brand mobile phones are likely to be a good strategy"
    else:
    	rec_brand = "No specific Interest in Top Brands"
    # print(style.BOLD+'2. Based on Type of User!!'+style.END)
    category = pd.DataFrame(classisfying_user.query('ID=='+str(ID))['category']).reset_index(drop=True)
    category = list(category.category)[0]
    # print('The above person is a '+category)
    # print('Hence mobile phones that could be Recommended to him are ')
    temp1=pd.DataFrame(temp.query('category=='+'"'+str(category)+'"'))
    temp1=temp1.drop_duplicates(subset="Model",keep='first')
    temp1 = temp1.head(3)
    # print(list(temp1.Model))
    print(style.BOLD+'3. Based on his Interest in <strong>Camera</strong>!!'+style.END)
    camera_type=pd.DataFrame(Camera_Lover.query('ID=='+str(ID))['Type']).reset_index(drop=True)
    camera_type = list(camera_type.Type)[0]
    if camera_type != 'Sensible':
        temp2=pd.DataFrame(temp_camera.query('Type=='+'"'+str(camera_type)+'"'))
        temp2=temp2.drop_duplicates(subset="Model",keep='first')
        temp2 = temp2.head(3)
        # rec_cam = 'He is a Camera Lover i.e '+ camera_type +'and thus following phones can be recommended'
        rec_cam = list(temp2.Model)
   
    else:
        rec_cam = "No specific Interest in Cameras"

     
    x=df.loc[df['ID']==ID]
    Models=list(x.Model.unique())
    Count=int(x.Count.unique())
    data={"ID":id,"Mobile_Purchased":Models,"Total_Purchased":Count}


    predictions = {
    	"categories" : [
    		{
    			"desp":"Recommend on basis of his interest in BRANDS",
    			"name":rec_brand
    		},
    		{
    			"desp":"BASED ON PERFORMANCE SCORE (USER CATEGORY)",
    			"name":list(temp1.Model)
    		},
    		{
    			"desp":"BASED ON INTEREST IN BRANDS (USER CATEGORY)",
    			"name":rec_cam
    		},
        
    	]
    }
    print("predictions")
    print(predictions)
    return predictions

def get_user_details(id):
    x=df.loc[df['ID']==id]
    Models=list(x.Model.unique())
    Count=int(x.Count.unique())
    data={"ID":id,"Mobile_Purchased":Models,"Total_Purchased":Count}
    return data

# APIS





from flask import Flask, request, jsonify, Response
import json
import pickle
from sklearn.externals import joblib

app = Flask(__name__)
CORS(app)
@app.route('/api/get_category_of_user',methods=['POST'])
def get():
    return get_user_details(request.get_json(force=True)['id'])

@app.route('/api/get_category_of_user',methods=['GET'])
def get_category_of_user():
	x = pd.DataFrame(classisfying_user['category'].value_counts())
	x.to_json(orient='split')
	data = {
  		"total": classisfying_user.shape[0],
    	"categories": [
        	{"name" : "Flagship Killers","value":int(x['category'][0])},
        	{"name": "Tech Savvy"      ,"value":int(x['category'][1])},
        	{"name": "Reasonable Brand Seekers"      ,"value":int(x['category'][2])},
        	{"name": "Budget Oriented"      ,"value":int(x['category'][3])},
        	{"name":  "Luxurious"      ,"value":int(x['category'][4])}
    	],
    	"description": "Different Categories of Users",
    	"x_axis":"User Categories",
    	"y_axis":"Number of Users"
	}
	return data


@app.route('/api/type_of_user',methods=['GET'])
def get_type_of_user():
	x = pd.DataFrame(Offers.Type.value_counts())
	data = {
  		"total": classisfying_user.shape[0],
    	"categories": [
    		{"name" : "Intermediate Customer","value":int(x['Type'][0])},
    		{"name" : "Regular Customer","value":int(x['Type'][1])}
    	],
    	"description": "User Type (Number of Purchases)",
    	"x_axis":"User Types",
    	"y_axis":"Number of Purchases"
		}
	return data


@app.route('/api/country/all', methods=['GET'])
def get_all_country():
	x = df.Country.unique().tolist()
	data = {
    "total": len(x),
    "countries": x
	}
	return data

@app.route('/api/country/details', methods=['POST'])
def get_country_details():
	country = request.get_json(force=True)['country']
	print(request.get_json(force=True))
	plot = df.loc[df['Country']==country]
	plot = pd.DataFrame(plot.groupby('Brand')['ID'].nunique()).reset_index()
	plot.rename(columns={'ID':'count'},inplace=True)
	temp = []
	for t in plot.Brand:
		tem = {
			"name": t,
			"value": int(pd.DataFrame(plot.loc[plot.Brand == t]['count']).reset_index()['count'][0])
		}
		temp.append(tem)
	data = {
   		'country' : country,
    	'categories' : temp,
    	'description': 'Distribution of Mobile Brands in '+country,
    	"x_axis":"X",
    	"y_axis":"Y"
		}
	return data

@app.route('/api/purchase/counts', methods=['GET'])
def get_purchase_details():
	temp = []
	plot = pd.DataFrame(df.Count.value_counts()).reset_index().sort_values(by='index').reset_index(drop=True)
	for t in range(1,12):
		if t == 8:
			print("")
		else:
			tem = {
			"name":t,
			"value":int(pd.DataFrame(plot.loc[plot['index'] == t]['Count']).reset_index().drop(['index'],axis=1)['Count'][0])
			}
			temp.append(tem)
	data = {
		"description" : "Number of Purchases - User Count",
		"categories" : temp,
		"x_axis":"No of Purchases",
		"y_axis":"Frequency"
	}
	return data

@app.route('/api/ram/counts', methods=['GET'])
def get_ram_details():
	temp = []
	plot = pd.DataFrame(df.RAM.value_counts()).reset_index().sort_values(by='index').reset_index(drop=True)
	for i in range(0,plot.shape[0]):
		tem = {
			"name":int(plot['index'][i]),
			"value":int(plot['RAM'][i])
			}
		temp.append(tem)
	data = {
		"description" : "Distribution of RAM (User Purchase) in GegaBytes",
		"categories" : temp,
		"x_axis":"RAM in GegaBytes",
		"y_axis":"Number of Purchases"
	}
	return data
@app.route('/api/storage/counts', methods=['GET'])
def get_storage_details():
	temp = []
	plot = pd.DataFrame(df.Storage.value_counts()).reset_index().sort_values(by='index').reset_index(drop=True)
	for i in range(0,plot.shape[0]):
		tem = {
			"name":int(plot['index'][i]),
			"value":int(plot['Storage'][i])
			}
		temp.append(tem)
	data = {
		"description" : "Distribution of Storage (User Purchase) in  GegaBytes",
		"categories" : temp,
		"x_axis":"Storage in GegaBytes",
		"y_axis":"Number of Purchases"
	}
	return data
@app.route('/api/front_camera/counts', methods=['GET'])
def get_front_camera_details():
	temp = []
	plot = pd.DataFrame(df['Front Camera'].value_counts()).reset_index().sort_values(by='index').reset_index(drop=True)
	for i in range(0,plot.shape[0]):
		tem = {
			"name":int(plot['index'][i]),
			"value":int(plot['Front Camera'][i])
			}
		temp.append(tem)
	data = {
		"description" : "Distribution of Front Camera (User Purchase) in  MegaPixels",
		"categories" : temp,
		"x_axis":"Front Camera in Megapixels",
		"y_axis":"Number of Purchases"
	}
	return data
@app.route('/api/rear_camera/counts', methods=['GET'])
def get_rear_camera_details():
	temp = []
	plot = pd.DataFrame(df['Rear Camera'].value_counts()).reset_index().sort_values(by='index').reset_index(drop=True)
	for i in range(0,plot.shape[0]):
		tem = {
			"name":int(plot['index'][i]),
			"value":int(plot['Rear Camera'][i])
			}
		temp.append(tem)
	data = {
		"description" : "Distribution of Rear Camera (User Purchase) in  MegaPixels",
		"categories" : temp,
		"x_axis":"Rear Camera in Megapixels",
		"y_axis":"Number of Purchases"
	}
	return data
@app.route('/api/payment/details', methods=['GET'])
def get_payment_details():
	x = pd.DataFrame(df.Payment_Type.value_counts()).reset_index()
	data = {
    "total": classisfying_user.shape[0],
    "categories": [
    	{"name" : "Visa","value":int(x['Payment_Type'][0])},
    	{"name" : "Mastercard","value":int(x['Payment_Type'][1])},
    	{"name" : "Amex","value":int(x['Payment_Type'][2])},
    	{"name" : "Diners","value":int(x['Payment_Type'][3])}
        ],
    "description": "Distribution - Mode of payment",
    "x_axis":"Payment Type",
    "y_axis":"Number of Purchases"
    }
	return data


@app.route('/api/feature/details', methods=['POST'])
def get_feature_details():
	feature = request.get_json(force=True)['feature']
	x = pd.DataFrame(df[feature].value_counts()).reset_index().sort_values(by='index').reset_index()
	x = x.rename(columns={'index':'size'})
	x.drop(['level_0'], axis=1, inplace=True)
	temp = []
	for t in x['size'].tolist():
		tem = {
		t: int(pd.DataFrame(x.loc[x['size'] == int(t)][feature]).reset_index()[feature][0])
		}
		temp.append(tem)
	data = {
		'data' : temp
		}
	return data


@app.route('/api/processor/all', methods=['GET'])
def get_all_processor():
	x = df.Processor.unique().tolist()
	data = {
    "total": len(x),
    "processor": x
	}
	return data
@app.route('/api/brand/all', methods=['GET'])
def get_all_brand():
	x = df.Brand.unique().tolist()
	data = {
    	"total": len(x),
    	"brand": x
		}
	return data

@app.route('/api/ram/all', methods=['GET'])
def get_all_ram():
	x = df.RAM.unique().tolist()
	data = {
    "total": len(x),
    "ram": x
	}
	return data


@app.route('/api/city/all', methods=['GET'])
def get_all_city():
	x = df.City.unique().tolist()
	data = {
    "total": len(x),
    "cities": x
	}
	return data

@app.route('/api/states/all', methods=['GET'])
def get_all_state():
	x = df.State.unique().tolist()
	data = {
    "total": len(x),
    "states": x
	}
	return data

@app.route('/api/states', methods=['POST'])
def get_state():
    city = request.get_json(force=True)['city']
    x = df.loc[df['City']==city]['State'].unique().tolist()
    data = {
    "total": len(x),
    "states": x
    }
    return data

@app.route('/api/cities', methods=['POST'])
def get_cities():
    state = request.get_json(force=True)['state']
    x = df.loc[df['State']==state]['City'].unique().tolist()
    data = {
    "total": len(x),
    "cities": x
    }
    return data

@app.route('/api/battery/all', methods=['GET'])
def get_all_battery():
	x = df.Battery.unique().tolist()
	data = {
    "total": len(x),
    "battery": x
	}
	return data

@app.route('/api/storage/all', methods=['GET'])
def get_all_storage():
	x = df.Storage.unique().tolist()
	data = {
    "total": len(x),
    "storage": x
	}
	return data
@app.route('/api/front_camera/all', methods=['GET'])
def get_all_front():
	x = df['Front Camera'].unique().tolist()
	data = {
    "total": len(x),
    "front_camera": x
	}
	return data
@app.route('/api/id/all', methods=['GET'])
def get_all_ID():
	x = df['ID'].unique().tolist()
	x.sort()
	data = {
    "id": x
	}
	return data
@app.route('/api/rear_camera/all', methods=['GET'])
def get_all_rear():
	x = df['Rear Camera'].unique().tolist()
	data = {
    "total": len(x),
    "rear_camera": x
	}
	return data

@app.route('/api/predict/score', methods=['POST'])
def predict_score():
	ram = request.get_json(force=True)['ram']
	storage = request.get_json(force=True)['storage']
	processor = request.get_json(force=True)['processor']
	battery = request.get_json(force=True)['battery']
	X = [[processor],[ram],[storage],[battery]]
	X[0] = labelencoder_predict_score_X.transform(X[0])
	predict_X = onehotencoder_predict_score_X.transform([[X[0][0],X[1][0],X[2][0],X[3][0]]]).toarray()
	predict_X = predict_X[:,1:]
	predict_X = sc_predict_score_X.transform(predict_X)
	with graph.as_default():	
		predictions = classifier_predict_score.predict(predict_X)
	predicted_score = sc_predict_score_y.inverse_transform(predictions)
	predicted_score = predicted_score[0][0]
	predict_category = predict_user(predicted_score)
	predictions = {
		"score":str(predicted_score),
		"category":predict_category
		}
	return predictions



	



@app.route('/api/predict/brand', methods=['POST'])
def predict_brand():
	city = request.get_json(force=True)['city']
	state = request.get_json(force=True)['state']
	X = [[city],[state]]
	X[0] = label_encoder_x1.transform(X[0])
	X[1] = label_encoder_x2.transform(X[1])
	predict_X = onehotencoder_x1.transform([[X[0][0],X[1][0]]]).toarray()
	predict_X = predict_X[:,1:]
	predict_X = predict_X[:,0:-1]

	with graph.as_default():
		predictions = classifier.predict(predict_X)
	classes = np.argmax(predictions, axis=1)
	prediction = label_encoder_y.inverse_transform([classes[0]])[0]
	return prediction

@app.route('/api/predict/camera', methods=['POST'])
def predict_cam():
	front_camera = request.get_json(force=True)['front_camera']
	rear_camera = request.get_json(force=True)['rear_camera']
	confidence = (front_camera*rear_camera)/(predict_camera_lover['Front Camera'].max()*predict_camera_lover['Rear Camera'].max())
	X = [[front_camera,rear_camera,confidence]]
	X = sc_predict_camera_lover_X.transform(X)
	with graph.as_default():
		predictions = classifier_predict_camera_lover.predict(X)
	classes = np.argmax(predictions, axis=1)
	predictions = labelencoder_predict_camera_lover_y.inverse_transform([classes[0]])[0]
	return jsonify(predictions)



@app.route('/api/predict/mobile/categories', methods=['POST'])
def predict_everything():
	brand1 = request.get_json(force=True)['brand']
	processor = request.get_json(force=True)['processor']
	ram = request.get_json(force=True)['ram']
	storage = request.get_json(force=True)['storage']
	battery = request.get_json(force=True)['battery']
	front_camera = request.get_json(force=True)['front_camera']
	rear_camera = request.get_json(force=True)['rear_camera']
	print(type(brand1))
	if brand1 == "Apple" and "Samsung" and "LG":
		lover = brand1
	else:
		lover = 'Brand Lovers aren\'t Interested'


	score = predict_antutu_score(processor, ram, storage, battery)
	# score = sc_predict_score_y.inverse_transform(score)
	camera_specs = predict_camera(front_camera, rear_camera)
	print(camera_specs,brand1)
	if camera_specs == "Sensible":
		camera_specs= '<strong>Camera Lovers aren\'t Interested</strong>'
	else:
		camera_specs = '<strong>'+camera_specs+'</strong>'
	predictions = {
	"categories":[
    		{
    			"name":'<strong>'+str(predict_user(score))+'</strong>',
    			"desp":"Based on Performance Score (User Category)"
    		},
    		{
    			"name":camera_specs,
    			"desp":"Based On Interest in Camera (User Category)"
    		},
    		{
    			"name":lover,
    			"desp":"Based On Interest in Brands (User Category)"
    		}

    	]
    	}
	return predictions

@app.route('/api/predict/id/recommend', methods=['POST'])
def predict_recommend():
	id = request.get_json(force=True)['id']

	return predict_mobile_for_users(id)

 


@app.route('/api/get/name',methods=['POST'])
def get_name():
    names = pd.read_csv('datasets/name.csv')
    char = request.get_json(force=True)['char']
    names = names.loc[(names.Name.str.startswith(char.lower(), na=False))].head(6)
    dat = []
    for row in names.itertuples():
        t = {"ID":row.ID,"name":row.Name}
        dat.append(t)
    data = {
    "data":dat
        }
    return data

if __name__ == "__main__":
	app.run(debug=True)

# sublime.set_timeout(self.do, 1000)
