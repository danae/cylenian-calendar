import math

# Convert a Gregorian date to Julian Date Number
def to_jdn(date):
  # Assuming date is a tuple (year, month, day)
  (year,month,day) = date
  
  # Calculate the Julian Day
  a = math.trunc((14 - month) / 12)
  y = year + 4800 - a
  m = month + 12 * a - 3
  return day + math.trunc((153 * m + 2) / 5) + 365 * y + math.trunc(y / 4) - math.trunc(y / 100) + math.trunc(y / 400) - 32045
  
# Convert a Julian Date Number to Gregorian date
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
  return (year,month,day)
  