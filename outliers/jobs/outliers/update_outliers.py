from bson import ObjectId
from pymongo import MongoClient


def job_update_outliers():
    URI = 'mongodb://db:27017'
    with MongoClient(URI) as connection:
        print('Update outliers')
        db = connection['OSeM-api']
        # boxes_dict = {"_id": ObjectId('5391be52a8341554157792e9'), "exposure": "Highway 37"}
        # db.boxes.insert(boxes_dict)
        boxes_query = {'_id': ObjectId('5391be52a8341554157792e6')}
        new_values = {"$set": {"exposure": "test46245"}}
        db.boxes.update(boxes_query, new_values)
        # db.boxes.find_one()
        print('Finish outliers')
    return True
