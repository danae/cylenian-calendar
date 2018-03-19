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
  cylenian_dict = d.cylenian_date.__dict__.copy()
  cylenian_dict['format'] = d.cylenian_date.format()
  cylenian_dict['longFormat'] = d.cylenian_date.format_long()
  cylenian_dict['monthName'] =  cylenian.month_name(d.cylenian_date.month)

  gregorian_dict = d.gregorian_date.__dict__.copy()
  gregorian_dict['format'] = d.gregorian_date.format()

  moon_dict = d.moon.__dict__.copy()
  moon_dict['format'] = d.moon.format()

  # Create a response object
  return jsonify(jdn = d.jdn, cylenian_date = cylenian_dict, gregorian_date = gregorian_dict, moon = moon_dict)


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
  d = Date.today()
  return jsonify_date(d)
