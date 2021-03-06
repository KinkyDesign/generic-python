from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from tornado.escape import json_decode, json_encode
from ..entities.prediction_request import PredictionRequest
from ..entities.dataset import Dataset
from ..entities.dataentry import DataEntry
from ..helpers import model_decoder
import numpy as np


def decode(request):
    json_request = json_decode(request.body)
    pred_request = PredictionRequest(json_request['dataset'], json_request['rawModel'], json_request['additionalInfo'])
    input_series = pred_request.additionalInfo['fromUser']['inputSeries']
    independentFeatures = pred_request.additionalInfo['independentFeatures']
    shorted = []
    actualIndepFeatKeys = []
    # pred_request.dataset.features['key']
    for actual in input_series:
        for key in independentFeatures:
            if actual == independentFeatures[key]:
                for feature in pred_request.dataset['features']:
                    if feature['name'] == actual:
                        shorted.append(feature['key'])
                # shorted.append(key)
    dataEntryAll = []
    for dataEntry in pred_request.dataset['dataEntry']:
        dataEntryToInsert = []
        for key in shorted:
            dataEntryToInsert.append(dataEntry['values'][key])
        dataEntryAll.append(dataEntryToInsert)
    return dataEntryAll
