# suppress all warnings
import warnings
warnings.filterwarnings("ignore")

import ntic
import flask
from flask import request
from datetime import datetime as dt
import pandas as pd

def king_data():
    data = pd.read_csv('data.csv', names=['s', 'e', 'm']).set_index('m')
    series = pd.Series(index=range(data.s.min(), dt.now().year + 1))

    for m in data.index:
        series.loc[data.loc[m].s:data.loc[m].e] = m
    
    return series.loc

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    data = king_data()
    year = int(request.args['shit'])
    try:
        return data[year]
    except KeyError:
        return f'Invalid input ({series.index.min()} - {series.index.max()})'