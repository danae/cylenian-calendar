import collections
import gregorian

# The leap eras in a 100-era timespan
leap_eras = [4,12,21,37,46,54,71,79,87]

# The names of the Cylenian months
month_names = [
  "Elsy'ondleð", "Nae Boryeð", "Seniðin", 
  "Liðin Boryeð", "Emmiðiða", "Omilnin", 
  "Karðondleð", "Seðaneðr", "Liliðin", 
  "Liðin Maroo", "Fðileð", "Elseniðor", 
  "Naeð Molið"
]

# The Cylenian epoch as a Julian Date Number
epoch = gregorian.to_jdn(gregorian.GregorianDate(-1944,12,21))

# Create a named tuple for Cylenian dates
CylenianDate = collections.namedtuple("CylenianDate",["era","year","month","day"])

# Return whether an era is a leap era
def is_leap_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))

  # Return the value
  return ((era - 1) % 100 + 1) in leap_eras
  
# Return whether a year is a leap year (years 6 and 12 are leap years)
def is_leap_year(year):
  # Assert parameters
  if year not in range(1,13):
    raise ValueError("The year {:r} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  return year == 6 or year == 12
  
# Return the amount of days in an era
def days_in_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))
    
  # Return the value
  return 4383 - (1 if is_leap_era(era) else 0)
  
# Return the amount of days in a year (1~12)
def days_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:r} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  if is_leap_year(year):  
    return 392 if (year == 12 and not is_leap_era(era)) else 391
  else:
    return 360
  
# Return the amount of days in a month (1~12)
def days_in_month(era, year, month):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:r} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {:r} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))
    
  # Return the value
  if is_leap_year(year) and month == 13:
    return 32 if (year == 12 and not is_leap_era(era)) else 31
  else:
    return 30
  
# Return the amount of months in a year (1-12)
def months_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:r} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  return 13 if is_leap_year(year) else 12
  
# Convert a Cylenian date to a Julian Day Number
def to_jdn(date):
  # Assuming date is a CylenianDate tuple
  era, year, month, day = date
  
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:r} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:r} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {:r} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))
  if day not in range(1,days_in_month(era,year,month) + 1):
    raise ValueError("The day {:r} is not a valid day; days are in the range 1-30 (31 or 32 in leap years)".format(day))
  
  # Loop over the variables
  ed = sum(days_in_era(e) for e in range(1,era))
  yd = sum(days_in_year(era,y) for y in range(1,year))
  md = sum(days_in_month(era,year,m) for m in range(1,month))
  
  # Return the result
  return epoch + ed + yd + md + day - 1

# Convert a Julian Day Number to a Cylenian date
def from_jdn(jdn):
  # Assert parameters
  if jdn - epoch < 0:
    raise ValueError("The Julian Day Number {:r} is not a valid day; only days from {} are supported".format(jdn,epoch))
    
  # Initialize variables
  jdn = jdn - epoch
  era = year = month = day = 1
  
  # Get the variables
  while jdn >= days_in_era(era):
    jdn -= days_in_era(era)
    era = era + 1
  while jdn >= days_in_year(era,year):
    jdn -= days_in_year(era,year)
    year = year + 1
  while jdn >= days_in_month(era,year,month):
    jdn -= days_in_month(era,year,month)
    month = month + 1
  day = jdn + 1
    
  # Return the tuple
  return CylenianDate(era,year,month,day)

# Format a Cylenian date in short notation
def format(date):
  return "{0.era}.{0.year}.{0.month}.{0.day}".format(date)
  
# Format a Cylenian date in long notation
def format_long(date):
  return "{1} {0.day}, {0.era}E{0.year}".format(date,month_names[date.month - 1])
