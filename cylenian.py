from functools import total_ordering

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

# Return the name of a month
def month_name(month):
  return month_names[month - 1]

# The Cylenian epoch as a Julian Date Number (equals to 21 december 1946 BCE)
epoch = 1011384

# Return whether an era is a leap era
def is_leap_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))

  # Return the value
  return ((era - 1) % 100 + 1) in leap_eras

# Return whether a year is a leap year (years 6 and 12 are leap years)
def is_leap_year(year):
  # Assert parameters
  if year not in range(1,13):
    raise ValueError("The year {:d} is not a valid year; years are in the range 1-12".format(year))

  # Return the value
  return year == 6 or year == 12

# Return the amount of days in an era
def days_in_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))

  # Return the value
  return 4383 - (1 if is_leap_era(era) else 0)

# Return the amount of days in a year (1~12)
def days_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:d} is not a valid year; years are in the range 1-12".format(year))

  # Return the value
  if is_leap_year(year):
    return 392 if (year == 12 and not is_leap_era(era)) else 391
  else:
    return 360

# Return the amount of days in a month (1~12)
def days_in_month(era, year, month):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:d} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {:d} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))

  # Return the value
  if is_leap_year(year) and month == 13:
    return 32 if (year == 12 and not is_leap_era(era)) else 31
  else:
    return 30

# Return the amount of months in a year (1-12)
def months_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:d} is not a valid year; years are in the range 1-12".format(year))

  # Return the value
  return 13 if is_leap_year(year) else 12

# Convert a JDN to a Cylenian date
def jdn_to_cylenian(jdn):
  # Assert parameters
  if jdn - epoch < 0:
    raise ValueError("The Julian Day Number {} is not a valid day; only days from {} are supported".format(jdn,epoch))

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

  # Return the result
  return (era, year, month, day)

# Convert this Cylenian date to a JDN
def cylenian_to_jdn(era, year, month, day):
  # Assert fields
  if era <= 0:
    raise ValueError("The era {:d} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {:d} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {:d} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))
  if day not in range(1,days_in_month(era,year,month) + 1):
    raise ValueError("The day {:d} is not a valid day; days are in the range 1-30 (31 or 32 in leap years)".format(day))

  # Loop over the fields
  era_days = sum(days_in_era(e) for e in range(1,self,era))
  year_days = sum(days_in_year(era,y) for y in range(1,self.year))
  month_days = sum(days_in_month(era,year,m) for m in range(1,self.month))

  # Return the result
  return epoch + era_days + year_days + month_days + day - 1


# Cylenian date class
@total_ordering
class CylenianDate:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.days_since_epoch = jdn - epoch
    self.era, self.year, self.month, self.day = jdn_to_cylenian(jdn)

  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)

  # Format this Cylenian date in the short notation
  def format(self):
    return "{0.era}.{0.year}.{0.month}.{0.day}".format(self)

  # Format this Cylenian date in the long notation
  def format_long(self):
    return "{1} {0.day}, {0.era}E{0.year}".format(self,month_name(self.month))

  # Convert this Cylenian date to a string
  def __str__(self):
    return self.format_long()
