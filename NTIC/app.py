# suppress all warnings
import warnings
warnings.filterwarnings("ignore")

import flask
from flask import request
from datetime import datetime as dt
import pandas as pd

data = pd.read_csv('data.csv', names=['s', 'e', 'm']).set_index('m')
series = pd.Series(index=range(data.s.min(), dt.now().year + 1))

for m in data.index:
    series.loc[data.loc[m].s:data.loc[m].e] = m

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    year = int(request.args['year'])
    try:
        return series.loc[year]
    except KeyError:
        return f'Invalid input ({series.index.min()} - {series.index.max()})'