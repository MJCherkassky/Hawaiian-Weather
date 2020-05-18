#ALL DEPENDENCIES
from flask import Flask, jsonify
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd


#DB SETUP

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#FLASK SETUP

app = Flask(__name__)

#FLASK ROUTES
@app.route('/')
def home():
    return (
        f"Please follow the below routes to learn more:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipdata():
    last_date = session.query(func.max(Measurement.date)).all()
    last_date = last_date[0][0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    year_before_date = ((last_date - relativedelta(years = 1)).strftime('%Y-%m-%d'))
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before_date).order_by(Measurement.date.desc()).all()
    data = {date: prcp for date, prcp in query}
    return jsonify(data)

@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    stations = list(np.ravel(stations))
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    last_date2 = session.query(func.max(Measurement.date)).all()
    last_date2 = last_date2[0][0]
    last_date2 = dt.datetime.strptime(last_date2, '%Y-%m-%d').date()
    year_before_date2 = ((last_date2 - relativedelta(years = 1)).strftime('%Y-%m-%d'))
    query = session.query(Measurement.tobs).filter(Measurement.date >= year_before_date2).order_by(Measurement.date.desc()).all()
    data = list(np.ravel(query))
    return jsonify(data)

@app.route('/api/v1.0/<start>')
def start_temp(start):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()   
    return jsonify(temp_data)

@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    range_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    return jsonify(range_data)

if __name__ == "__main__":
    app.run(debug=True)