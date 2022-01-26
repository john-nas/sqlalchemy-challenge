import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

## create engine to hawaii.sqlite

engine = create_engine("sqlite:///hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
station = base.classes.station

## reflect an existing database into a new model
Base = automap_base()
## reflect the tables
Base.prepare(engine, reflect=True)

## Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

## Create our session (link) from Python to the DB
session = Session(engine)

## Find the most recent date in the data set.
session.query(measurement.date).order_by(measurement.date.desc()).first()

## Calculate the date one year from the last date in data set.
latest_date = dt.date(2017,8,23)
previous_year = latest_date - dt.timedelta(days=365)
previous_year

## Close session
session.close()

## Create an app
app = Flask(__name__)


## Define static routes
## Define landing page route with available pages

@app.route("/")
def welcome():
    return (f"Welcome to my Weather Analysis API<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitaton<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end"
            )

## Define precipitation page 

@app.route("/api/v1.0/precipitaton")
def precipitation():
## Create our session (link) from Python to the DB
    session = Session(engine)
## Perform a query to retrieve the data and precipitation scores
    precip_q = session.query(measurement.date, measurement.prcp)
## Close Session
    session.close()
  
## Create a dictionary from the row data and append to a list of precipitation_list
    precipitation = {}
    for i in precip_q:
        precipitation_list = {i.date: i.prcp, "prcp": i.prcp}
        precipitation.update(precipitation_list)

    return jsonify(precipitation)



## Define stations page 

@app.route("/api/v1.0/stations")
def stations():
    stations_list = session.query(station.station).all()
    stations_json = list(np.ravel(stations_list))
    return jsonify(stations_json) 
                   
## Define tobs (temperature observation) page

@app.route("/api/v1.0/tobs")
def temp_obs():                 
      
    tobs_list = session.query(station.name, measurement.date, measurement.tobs).\
        filter(station.station=='USC00519281').all()
    tobs_json = list(np.ravel(tobs_list))
    return jsonify(tobs_json)                   

## Define date_start page              
@app.route("/api/v1.0/<start>")
def date_start(start):
    start_list = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()               
    start_json = list(np.ravel(start_list))
    return jsonify(start_json)               

## Define date_start_end page                 
@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):                   
    end_list = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start, measurement.date <= end).all()
    end_json = list(np.ravel(end_list))
    return jsonify(end_json)        
        
if __name__ == '__main__':
    app.run(debug=True) 