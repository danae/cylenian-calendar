import gregorian
     
# The leap eras in a 100-era timespan
leap_eras = [4,12,21,37,46,54,71,79,87]

# Return whether an era is a leap era
def is_leap_era(era):
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))

   # Return if a leap era
  return ((era - 1) % 100 + 1) in leap_eras
  
# Return the amount of days in an era
def days_in_era(era):
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
    
  # Return the days in the era
  return 4383 - (1 if is_leap_era(era) else 0)
  
# Return the amount of days in a year (1~12)
def days_in_year(era, year):
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the days in the year
  if year == 6:
    return 391
  elif year == 12:
    return 392 - (1 if is_leap_era(era) else 0)
  else:
    return 360
  
# Return the amount of days in a month (1~12)
def days_in_month(era, year, month):
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,14):
    raise ValueError("The month {} is not a valid month; months are in the range 1-12".format(month))
    
  # Return the days in the month
  if year == 6 and month == 13:
    return 31
  elif year == 12 and month == 13:
    return 32
  else:
    return 30
  
# Return the amount of months in a year (1-12)
def months_in_year(era, year):
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
    
  # Return the months in the year
  if year == 6 or year == 12:
    return 13
  else:
    return 12
  
# Calculate the Cylenian date as a tuple from days since the epoch (era,year,month,day)
def tuple_from_days(days):
   # Initialize variables
  era = year = month = day = 1
  
  # Check if the parameters are valid
  if days < 0:
    raise ValueError("The day {} is not a valid day; only positive days are supported".format(day))
    
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
  return (era,year,month,day)
    
# Calculate the days since the epoch from a Cylenian date
def days_from_tuple(date):
  # Assuming date is a tuple (era,year,month,day)
  era = date[0]
  year = date[1]
  month = date[2]
  day = date[3]
  
  # Check if the parameters are valid
  if era <= 0:
    raise ValueError("The era {} is not a valid era; only positive eras are supported".format(era))
  if year not in range(1,13):
    raise ValueError("The year {} is not a valid year; years are in the range 1-12".format(year))
  if month not in range(1,14):
    raise ValueError("The month {} is not a valid month; months are in the range 1-13".format(month))
  if day not in range(1,33):
    raise ValueError("The day {} is not a valid day; days are in the range 1-32".format(day))
  
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
class date:
  # The Cylenian epoch as a Julian Date Number
  epoch = gregorian.to_jdn((-1944,12,21))
  
  # The names of the Cylenian months
  months = [
    "Elsy'ondleð", "Nae Boryeð", "Seniðin", 
    "Liðin Boryeð", "Emmiðiða", "Omilnin", 
    "Karðondleð", "Seðaneðr", "Liliðin", 
    "Liðin Maroo", "Fðileð", "Elseniðor", 
    "Naeð Molið"
  ]
  
  # Constructor
  def __init__(self, days_since_epoch):
    self.days_since_epoch = days_since_epoch
    self.tuple = tuple_from_days(days_since_epoch)
    
  # Return the date parts
  def era(self):
    return self.tuple[0]
  def year(self):
    return self.tuple[1]
  def month(self):
    return self.tuple[2]
  def day(self):
    return self.tuple[3]
    
  # Return the name of the month
  def name_of_month(self):
    return self.months[self.month() - 1]
    
  # Format this date in the short notation
  def format_short(self):
    return ".".join([str(t) for t in self.tuple])
    
  # Format this date in the long notation
  def format_long(self):
    return "{2} {3}, {0}E{1}".format(self.era(),self.year(),self.name_of_month(),self.day())
    
  # Return a Cylenian date tuple (e,y,m,d) representing this date
  def to_cylenian(self):
    return self.tuple
    
  # Return a Gregorian date tuple (y,m,d) representing this date
  def to_gregorian(self):
    return gregorian.from_jdn(self.days_since_epoch + self.epoch)
    
  # Return a Cylenian date representing the Cylenian date tuple
  @classmethod
  def from_cylenian(cls, date):
    return cls(days_from_tuple(date))
    
    # Return a Cylenian date representing this gregorian date
  @classmethod
  def from_gregorian(cls, date):
    return cls(gregorian.to_jdn(date) - cls.epoch)
    
  # Convert to string
  def __str__(self):
    return self.format_short()
  