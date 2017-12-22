import date
import datetime
from parse import parse
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS

# Encodes a Cylenian date into JSON
def jsonify_date(d):
  cylenian = {}
  cylenian['date'] = dict(zip(('era','year','month','day'),d.cylenian()))
  cylenian['daysSinceEpoch'] = d.days
  cylenian['format'] = {'short': d.format_short(), 'long': d.format_long(), 'nameOfMonth': d.name_of_month()}
  
  gregorian = {}
  gregorian['date'] = dict(zip(('year','month','day'),d.gregorian()))
  
  # Create a response object
  return jsonify(cylenian = cylenian, gregorian = gregorian)
  

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
@app.route('/days.json')
def days():
  # Get the request day
  day = request.args.get('day')
  if day is None:
    raise ValueError('No day argument was supplied')
  
  # Parse the date
  try:
    day = int(day)
  except ValueError:
    raise ValueError('The day is not a valid day; are you sure you entered a number?')
  
  # Convert the date to a Cylenian date
  d = date.Date(day)
  return jsonify_date(d)

# Get the date for a Cylenian representation
@app.route('/cylenian.json')
def cylenian():
  # Get the request date
  d = request.args.get('date')
  if d is None:
    raise ValueError('No date argument was supplied')
  
  # Parse the date
  d = parse("{:d}.{:d}.{:d}.{:d}",d)
  if d is None:
    raise ValueError('The date is not a valid date; only dates of the format "era.year.month.day" are allowed')
  
  # Convert the date to a Cylenian date
  d = cyleniandate.Date.from_cylenian(*d)
  return jsonify_date(d)

# Get the date for a Gregorian representation
@app.route('/gregorian.json')
def gregorian():
  # Get the request date
  d = request.args.get('date')
  if d is None:
    raise ValueError('No date argument was supplied')
  
  # Parse the date
  d = parse("{:04d}-{:02d}-{:02d}",d)
  if d is None:
    raise ValueError('The date is not a valid date; only dates of the format "year-month-day" are allowed')
  
  # Convert the date to a Cylenian date
  d = date.Date.from_gregorian(*d)
  return jsonify_date(d)

# Create a route for today
@app.route('/today.json')
def today():
  # Get the date of today
  today = datetime.date.today()
  today_tuple = today.timetuple()
  
  # Convert it to a Cylenian date
  d = date.Date.from_gregorian(today_tuple)
  return jsonify_date(d)
