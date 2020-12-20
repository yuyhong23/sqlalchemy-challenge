import sqlalchemy
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

from sqlalchemy.ext.automap import automap_base
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

from sqlalchemy.orm import Session

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation score 1 year ago"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= "2016-08-23").\
                    filter(Measurement.prcp.isnot(None)).\
                    order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary with date as key and prcp as value
    preciptations = []
    for result in results:
        precipitation_dict = {result.date: result.prcp}
        preciptations.append(precipitation_dict)

    return jsonify(preciptations)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query the stations
    results = session.query(Station.station).group_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    import numpy as np
    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

if __name__ == '__main__':
    app.run(debug=True)
