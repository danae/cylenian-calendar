import functools
import gregorian
import season
     
# The leap eras in a 100-era timespan
LEAP_ERAS = [4,12,21,37,46,54,71,79,87]

# The names of the Cylenian months
NAME_OF_MONTHS = [
  "Elsy'ondleð", "Nae Boryeð", "Seniðin", 
  "Liðin Boryeð", "Emmiðiða", "Omilnin", 
  "Karðondleð", "Seðaneðr", "Liliðin", 
  "Liðin Maroo", "Fðileð", "Elseniðor", 
  "Naeð Molið"
]

# The Cylenian epoch as a Julian Date Number
EPOCH_JDN = gregorian.to_jdn(-1944,12,21)


# Return whether an era is a leap era
def is_leap_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))

  # Return the value
  return ((era - 1) % 100 + 1) in LEAP_ERAS
  
# Return whether a year is a leap year (years 6 and 12 are leap years)
def is_leap_year(year):
  # Assert parameters
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  return year == 6 or year == 12
  
# Return the amount of days in an era
def days_in_era(era):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
    
  # Return the value
  return 4383 - (1 if is_leap_era(era) else 0)
  
# Return the amount of days in a year (1~12)
def days_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  if is_leap_year(year):
    return 392 if (year == 12 and not is_leap_era(era)) else 391
  else:
    return 360
  
# Return the amount of days in a month (1~12)
def days_in_month(era, year, month):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))
    
  # Return the value
  if is_leap_year(year) and month == 13:
    return 32 if (year == 12 and not is_leap_era(era)) else 31
  else:
    return 30
  
# Return the amount of months in a year (1-12)
def months_in_year(era, year):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the value
  return 13 if is_leap_year(year) else 12
  
# Calculate the Cylenian date as a tuple from days since the epoch (era,year,month,day)
def from_days(days):
  # Assert parameters
  if days < 0:
    raise ValueError("The day {} is not a valid day; only non-negative days are supported".format(day))
    
  # Initialize variables
  era = year = month = day = 1
  
  # Get the variables
  while days >= days_in_era(era):
    days -= days_in_era(era)
    era = era + 1
  while days >= days_in_year(era,year):
    days -= days_in_year(era,year)
    year = year + 1
  while days >= days_in_month(era,year,month):
    days -= days_in_month(era,year,month)
    month = month + 1
  day = days + 1
    
  # Return the tuple
  return era, year, month, day
    
# Calculate the days since the epoch from a Cylenian date
def to_days(era, year, month, day):
  # Assert parameters
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,13 + (1 if is_leap_year(year) else 0)):
    raise ValueError("The month {} is not a valid month; months are in the range 1-12 (13 in leap years)".format(month))
  if day not in range(1,days_in_month(era,year,month) + 1):
    raise ValueError("The day {} is not a valid day; days are in the range 1-30 (31 or 32 in leap years)".format(day))
  
  # Initialize variables
  days = 0
  
  # Loop over the variables
  for e in range(1,era):
    days += days_in_era(e)
  for y in range(1,year):
    days += days_in_year(era,y)
  for m in range(1,month):
    days += days_in_month(era,year,m)
  days += day - 1
  
  # Return the days
  return days
  
  
# Date class
@functools.total_ordering
class Date:
  
  # Constructor
  def __init__(self, days):
    self.days = days
    self.tuple = from_days(days)
    self.gregorian_tuple = gregorian.from_jdn(self.days + EPOCH_JDN)
    print(self)
    
  # Return the date parts
  def era(self):
    return self.tuple[0]
  def year(self):
    return self.tuple[1]
  def month(self):
    return self.tuple[2]
  def name_of_month(self):
    return NAME_OF_MONTHS[self.month() - 1]
  def day(self):
    return self.tuple[3]  
    
  # Comparison operators
  def __eq__(self, other):
    return self.days == other.days
  def __lt__(self, other):
    return self.days < other.days
  def __hash__(self):
    return hash(self.days)
    
  # Return a Cylenian date tuple representing this date
  def cylenian(self):
    return self.tuple
    
  # Return a Gregorian date tuple representing this date
  def gregorian(self):
    return self.gregorian_tuple
    
  # Format this date in the two common notations
  def format_short(self):
    return ".".join([str(t) for t in self.tuple])
  def format_long(self):
    return "{2} {3}, {0}E{1}".format(self.era(),self.year(),self.name_of_month(),self.day())
  
  # Convert to string
  def __str__(self):
    return self.format_long()
    
  # Return a Cylenian date representing this Cylenian date
  @classmethod
  def from_cylenian(cls, era, year, month, day):
    return cls(to_days(era,year,month,day))
    
  # Return a Cylenian date representing this Gregorian date
  @classmethod
  def from_gregorian(cls, year, month, day):
    return cls(gregorian.to_jdn(year,month,day) - EPOCH_JDN)
