import bisect
import collections
import gregorian

# Create a named tuple for Gregorian dates
SeasonDate = collections.namedtuple("SeasonDate",["year","season","day"])

# Names of seasons
season_names = ["spring","summer","autumn","winter"]
# Month-Day pairs for the start of seasons
season_starts = [(3,21), (6,21), (9,21), (12,21)]
# Dict to combine names and start dates
seasons = dict(zip(season_names,season_starts))

# Return the year and season for a Gregorian date
def get_season(date):
  # Assuming date is a GregorianDate tuple
  monthday = date[1:3]

  # Get the insort index for the month-day pair
  season_index = bisect.bisect(season_starts,monthday) - 1
  
  # Get the season
  if season_index >= 0:
    return date.year, season_names[season_index]
  else:
    return date.year - 1, season_names[-1]
    
# Convert a season date to a Gregorian date
def to_gregorian(season):
  # Get the start of the season as a GregorianDate
  season_start = gregorian.GregorianDate(season.year,*seasons[season.season])
  season_start_jdn = gregorian.to_jdn(season_start)
  
  # Add the day number to the date
  jdn = season_start_jdn + season.day - 1
  
  # Return the value
  return gregorian.from_jdn(jdn)

# Convert a Gregorian date to a season date
def from_gregorian(date):
  # Assuming date is a GregorianDate tuple
  year, month, day = date
    
  # Return the value
  season = get_season(date)
  season_start = gregorian.GregorianDate(season[0],*seasons[season[1]])
  day = gregorian.difference(season_start,date) + 1
  return SeasonDate(*season,day)
  
# Get the ordinal for a number
def ordinal(num):
  num = num if num < 20 else (num % 10)
  if num == 1:
    return "st"
  elif num == 2:
    return "nd"
  elif num == 3:
    return "rd"
  else:
    return "th"
  
# Format a Season date
def format(date):
  return "{}, {}{} day of {}".format(date.year,date.day,ordinal(date.day),str.capitalize(date.season))
