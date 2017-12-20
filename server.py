import cyleniandate
import datetime
from parse import parse
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS

# Encodes a Cylenian date into JSON
def jsonify_date(date):
  cylenian = {}
  cylenian['date'] = dict(zip(('era','year','month','day'),date.to_cylenian()))
  cylenian['daysSinceEpoch'] = date.days_since_epoch
  cylenian['format'] = {'short': date.format_short(), 'long': date.format_long(), 'nameOfMonth': date.name_of_month()}
  
  gregorian = {}
  gregorian['date'] = dict(zip(('year','month','day'),date.to_gregorian()))
  
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
  day = int(day)
  #if date is None:
    #raise ValueError('The date is not a valid date; only dates of the format "era.year.month.day" are allowed')
  
  # Convert the date to a Cylenian date
  date = cyleniandate.date(day)
  return jsonify_date(date)

# Get the date for a Cylenian representation
@app.route('/cylenian.json')
def cylenian():
  # Get the request date
  date = request.args.get('date')
  if date is None:
    raise ValueError('No date argument was supplied')
  
  # Parse the date
  date = parse("{:d}.{:d}.{:d}.{:d}",date)
  if date is None:
    raise ValueError('The date is not a valid date; only dates of the format "era.year.month.day" are allowed')
  
  # Convert the date to a Cylenian date
  date = cyleniandate.date.from_cylenian(date)
  return jsonify_date(date)

# Get the date for a Gregorian representation
@app.route('/gregorian.json')
def gregorian():
  # Get the request date
  date = request.args.get('date')
  if date is None:
    raise ValueError('No date argument was supplied')
  
  # Parse the date
  date = parse("{:04d}-{:02d}-{:02d}",date)
  if date is None:
    raise ValueError('The date is not a valid date; only dates of the format "year-month-day" are allowed')
  
  # Convert the date to a Cylenian date
  date = cyleniandate.date.from_gregorian(date)
  return jsonify_date(date)

# Create a route for today
@app.route('/today.json')
def today():
  # Get the date of today
  today = datetime.date.today()
  today_tuple = today.timetuple()
  
  # Convert it to a Cylenian date
  date = cyleniandate.date.from_gregorian(today_tuple)
  return jsonify_date(date)
