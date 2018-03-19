from functools import total_ordering
from math import trunc

# Return whether a year is a leap year
def is_leap_year(year):
  # Return the value
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Return the amount of days in a month
def days_in_month(year, month):
  # Assert parameters
  if month not in range(1,13):
    raise ValueError("The month {:d} is not a valid month; months are in the range 1-12".format(month))

  # Return the value
  if month == 2:
    return 29 if is_leap_year(year) else 28
  else:
    return 31 if month in [1,3,5,7,8,10,12] else 30

# Convert a JDN to a Gregorian date
def jdn_to_gregorian(jdn):
  # Calculate the Gregorian date from the JDN
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

  # Return the result
  return (year, month, day)

# Convert a Gregorian date to a JDN
def gregorian_to_jdn(year, month, day):
  # Assert parameters
  if month not in range(1,13):
    raise ValueError("The month {:d} is not a valid month; months are in the range 1-12".format(month))
  if day not in range(1,days_in_month(year,month) + 1):
    raise ValueError("The day {:d} is not a valid day; days are in the range 1-31, depending on the month".format(day))

  # Calculate the JDN
  a = trunc((14 - month) / 12)
  y = year + 4800 - a
  m = month + 12 * a - 3
  return day + trunc((153 * m + 2) / 5) + 365 * y + trunc(y / 4) - trunc(y / 100) + trunc(y / 400) - 32045


# GregorianDate class
@total_ordering
class GregorianDate:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.year, self.month, self.day = jdn_to_gregorian(jdn)

  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)

  # Format this Gregorian date
  def format(self):
    return "{0.year:04d}-{0.month:02d}-{0.day:02d}".format(self)

  # Convert this Gregorian date to a string
  def __str__(self):
    return self.format()
