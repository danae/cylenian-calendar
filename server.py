import datetime
from parse import parse
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS

import cylenian
import gregorian
from date import Date

# Encodes a Cylenian date into JSON
def jsonify_date(d):
  cylenian_dict = {}
  cylenian_dict['era'] = d.cylenian_date.era
  cylenian_dict['year'] = d.cylenian_date.year
  cylenian_dict['month'] = d.cylenian_date.month
  cylenian_dict['day'] = d.cylenian_date.day
  cylenian_dict['daysSinceEpoch'] = d.jdn - cylenian.epoch
  cylenian_dict['format'] = d.format_cylenian()
  cylenian_dict['longFormat'] = d.format_cylenian_long()
  cylenian_dict['monthName'] =  cylenian.month_names[d.cylenian_date.month - 1]
  
  gregorian_dict = {}
  gregorian_dict['year'] = d.gregorian_date.year
  gregorian_dict['month'] = d.gregorian_date.month
  gregorian_dict['day'] = d.gregorian_date.day
  gregorian_dict['format'] = d.format_gregorian()
  
  season_dict = {}
  season_dict['year'] = d.season_date.year
  season_dict['season'] = d.season_date.season
  season_dict['day'] = d.season_date.day
  season_dict['format'] = d.format_season()
  
  # Create a response object
  return jsonify(jdn = d.jdn, cylenianDate = cylenian_dict, gregorianDate = gregorian_dict, season = season_dict)
  

# Create a Flask application
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Register an error handler for ValueErrors
@app.errorhandler(ValueError)
def value_error(error):
  response = jsonify({'error': ','.join(error.args)})
  response.status_code = 400
  return response
  
# Get the date for days since epoch
@app.route('/days/<day>')
def days(day):
  d = Date(day)
  return jsonify_date(d)

# Get the date for a Cylenian representation
@app.route('/cylenian/<int:era>/<int:year>/<int:month>/<int:day>')
def cylenian_date(era, year, month, day):
  d = Date.from_cylenian(cylenian.CylenianDate(era,year,month,day))
  return jsonify_date(d)

# Get the date for a Gregorian representation
@app.route('/gregorian/<int:year>/<int:month>/<int:day>')
def gregorian_date(year, month, day):
  d = Date.from_gregorian(gregorian.GregorianDate(year,month,day))
  return jsonify_date(d)

# Create a route for today
@app.route('/today')
def today():
  # Get the date of today
  today = datetime.date.today()
  today_tuple = today.timetuple()[:3]
  
  # Convert it to a Cylenian date
  d = Date.from_gregorian(today_tuple)
  return jsonify_date(d)
