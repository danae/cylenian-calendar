import collections
import math

# Create a named tuple for Gregorian dates
GregorianDate = collections.namedtuple("GregorianDate",["year","month","date"])

# Return whether a year is a leap year
def is_leap_year(year):
  # Return the value
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
# Return the amount of days in a month
def days_in_month(year, month):
  # Assert parameters
  if month not in range(0,13):
    raise ValueError("The month {} is not a valid month; months are in the range 1-12".format(month))
    
  # Return the value
  if month == 2:
    return 29 if is_leap_year(year) else 28
  else:
    return 31 if month in [1,3,5,7,8,10,12] else 30

# Convert a Gregorian date to a Julian Date Number
def to_jdn(date):
  # Assuming date is a GregorianDate tuple
  year, month, day = date

  # Assert parameters
  if month not in range(0,13):
    raise ValueError("The month {} is not a valid month; months are in the range 1-12".format(month))
  if day not in range(1,days_in_month(year,month) + 1):
    raise ValueError("The day {} is not a valid day; days are in the range 1-31, depending on the month".format(day))
  
  # Calculate the Julian Day
  a = math.trunc((14 - month) / 12)
  y = year + 4800 - a
  m = month + 12 * a - 3
  return day + math.trunc((153 * m + 2) / 5) + 365 * y + math.trunc(y / 4) - math.trunc(y / 100) + math.trunc(y / 400) - 32045
  
# Convert a Julian Date Number to a Gregorian date
def from_jdn(jdn):
  # Calculate the Gregorian date
  j = jdn + 32044
  g = j // 146097
  dg = j % 146097
  c = (dg // 36524 + 1) * 3 // 4
  dc = dg - c * 36524
  b = dc // 1461
  db = dc % 1461
  a = (db // 365 + 1) * 3 // 4
  da = db - a * 365
  y = g * 400 + c * 100 + b * 4 + a
  m = (da * 5 + 308) // 153 - 2
  d = da - (m + 4) * 153 // 5 + 122
  year = y - 4800 + (m + 2) // 12
  month = (m + 2) % 12 + 1
  day = d + 1
  
  # Create a tuple of the result
  return GregorianDate(year,month,day)
