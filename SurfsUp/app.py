# 1. Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement

Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

# 2. Create an app
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def percipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all percipitation analysis"""
    # Query all percipitation observation for the last year

    percp_date=session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()

    #Closing Session
    session.close()

    # Create a dictionary from the row data and append to a list pericipitation
    
    percipitation_analysis = []
    for date, prcp in percp_date:
        percp_dict = {}
        percp_dict["date"] = date
        percp_dict["prcp"] = prcp
       
        percipitation_analysis.append(percp_dict)

    return jsonify(percipitation_analysis)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station name """
    # Query all active station
   
    station_name = session.query(Station.station).all()
    #Closing Session
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(station_name))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observation of most active station in the previous year"""
    #  Query the dates and temperature observations of the most-active station for the previous year of data.
    
    last_year_tobs=session.query(Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').filter(Measurement.station =="USC00519281").\
    order_by(Measurement.station).all()

    #Closing Session
    session.close()
    all_tobs = list(np.ravel(last_year_tobs))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    #  Query minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range

    temperature_stats=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()
    stats = list(np.ravel(temperature_stats))

    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start,end):

     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    #  Query minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range

    temperature_stats=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    
    session.close()
    stats = list(np.ravel(temperature_stats))

    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)