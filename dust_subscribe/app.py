#!/usr/bin/env python

import json
import flask
import numpy as np
import sqlite3
import random
import os

from flask import render_template 


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


# global variable
ndata = 0
rows = 0
cs = 0

# color select
def colorSelect(val):
    if val >= 17:
        return 0.8
    elif val < 17:
        return 0.1
    else:
        return 0.5

def dbConnect():
    
    global ndata, rows

    con = sqlite3.connect('dustData.db')
    con.row_factory=sqlite3.Row
    cs = con.cursor()
    cs.execute('SELECT * FROM t1')
        
    rows = cs.fetchall(); 
    ndata = len(rows)
    return None


@app.route("/")
def basic():
    
    return render_template('index.html')



@app.route("/data")
@app.route("/data/<int:ndata>")
def data():
    
    global ndata, rows
   
    print(ndata)
    
    dbConnect()
    c = []
    rows = np.array(rows)
    
    for j in range(ndata):
        c.append(colorSelect(int(rows[j][0])))
    
    return json.dumps([{"_id": i, "x": rows[i][1], "y": rows[i][2], "pmdata": rows[i][0],
        "color": c[i]}
        for i in range(ndata)])


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000, debug=True) 
    #socket.run(app, host='0.0.0.0', port=5000, debug=True)
