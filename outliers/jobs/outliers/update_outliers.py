import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import datetime
from pymongo import MongoClient


def job_update_outliers():
    URI = 'mongodb://db:27017'
    with MongoClient(URI) as connection:
        db = connection['OSeM-api']

        # phenomena = ['rel. Luftfeuchte']
        phenomena = ['PM10', 'PM2.5', 'Temperatur', 'rel. Luftfeuchte', 'Luftfeuchtigkeit', 'Luftfeuchte']
        for phenomenon in phenomena:
            df_measurements = get_df_measurements(db, phenomenon)

            if df_measurements.empty:
                return

            model = regression_model(df_measurements)
            cd = cook_distance(model)
            ids = []
            count = 0
            for element in cd:
                if (element > 4 / len(df_measurements.index)):  # Using cook's distance formula
                    ids.append(count)
                count += 1
            # Return influential temperature values
            influential_temp_values = df_measurements[df_measurements.index.isin(ids)]
            print(influential_temp_values['_id'], influential_temp_values['sensor_id'], influential_temp_values['value'])
            sensors = (influential_temp_values['_id']).to_list()
            update_outliers(db, sensors)


def update_outliers(db, sensors):
    # measurements_query = {'_id': {'$in': sensors}}
    new_values = {"$set": {"is_outlier": True}}
    # db.measurements.update({'_id': {'$in': [sensors[1]]}}, new_values)
    for sensor in sensors:
        measurements_query = {'_id': sensor}
        db.measurements.update(measurements_query, new_values)
    print('Update outliers')


def get_df_measurements(db, phenomenon):
    exposure = 'outdoor'
    boxes_query = {
        'sensors.title': phenomenon,
        'exposure': exposure
    }

    boxes = db.boxes.find(boxes_query)
    sensors = []
    for box in boxes:
        for sensor in box['sensors']:
            if sensor['title'] == phenomenon:
                sensors.append(sensor['_id'])

    from_date = datetime(2019, 7, 28, 10, 8, 30, 125000)
    to_date = datetime(2019, 7, 31, 10, 9, 30, 125000)

    measure_query = {
        'sensor_id': {'$in': sensors},
        # 'createdAt': {'$gt': from_date, '$lt': to_date}
    }

    db_measurements = db.measurements.find(measure_query)
    measurements = []
    for measurement in db_measurements:
        if measurement['value']:
            measurements.append({
                '_id': measurement['_id'],
                'sensor_id': measurement['sensor_id'],
                'value': float(measurement['value']),
                'location': measurement['location'],
                'createdAt': int(measurement["createdAt"].strftime('%Y%m%d'))
            })
    # create dataset
    df_measurements = pd.DataFrame(measurements)
    return df_measurements


# Regression Model
def regression_model(temp_df):
    # define response variable
    y = temp_df['value']

    # define explanatory variable
    x = temp_df[['createdAt']]

    # add constant to predictor variables
    x = sm.add_constant(x)

    # fit linear regression model
    model = sm.OLS(y, x).fit()

    # view model summary
    return model


# Cook's distance
def cook_distance(model):
    # suppress scientific notation
    np.set_printoptions(suppress=True)

    # create instance of influence
    influence = model.get_influence()

    # obtain Cook's distance for each observation
    cooks = influence.cooks_distance

    # display Cook's distances
    cooksd = cooks[0]
    return cooksd
