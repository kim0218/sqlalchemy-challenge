# Import dependencies
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# # create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
#Base.classes.keys()

# # Save references to each table
Meas = Base.classes.measurement
Stat = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

###################################################################
# Setup Flask
##################################################################

app = Flask(__name__)

@app.route('/')
def home():
    return"""
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/<start><br>
    /api/v1.0/&lt;start&gt;/&lt;end&gt;
    """
@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return a list of all prcp names"""
    results = session.query(Meas.date, Meas.prcp).\
        filter(Meas.date >= '2016-08-23').\
        group_by(Meas.date).all()

    all_precipitation = []

    for result in results:
        precipitation_dict = {}
        precipitation_dict["date"] = result[0]
        precipitation_dict["prcp"] = result[1]
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""
    results = session.query(Meas.station).group_by(Meas.station).all()
    all_sessions = list(np.ravel(results))
    return jsonify(all_sessions)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations (tobs) for the previous year"""
    # Query all tobs for the previous year
    results = session.query(Meas.date, Meas.tobs).\
    filter(Meas.date >= '2016-08-23').all()

    all_tobs = []

    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result[0]
        tobs_dict["tobs"] = result[1]
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start date"""
    year, month, date = map(int, start.split('-'))
    date_start = dt.date(year,month,day)
    # Query for tobs of defined start date
    results = session.query(func.min(Meas.tobs),func.max(Meas.tobs).\
                            func.avg(Meas.tobs)).filter(Meas.date >= date_start).all()
    data = list(np.ravel(results))
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given range"""
    year, month, date = map(int, start.split('-'))
    date_start = dt.date(year,month,day)
    year2, month2, date2 = map(int, end.split('-'))
    date_end = dt.date(year2,month2,day2)
    # Query for tobs for definied date range
    results = session.query(func.min(Meas.tobs),func.max(Meas.tobs).\
                            func.avg(Meas.tobs)).filter(Meas.date >= date_start).filter(Meas.date <= date_end).all()
    data = list(np.ravel(results))
    return jsonify(data)    

if __name__ == '__main__':
    app.run(debug=True)