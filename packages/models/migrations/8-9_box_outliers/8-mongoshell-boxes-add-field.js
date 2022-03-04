/* eslint-disable */

// TODO add field is_outlier to measurements
db = db.getSiblingDB('OSeM-api');

db.measurements.update({},{ $set: {"is_outlier": false} },false,true);
