from functools import total_ordering
import bisect
import gregorian

# Names of seasons
season_names = ['spring','summer','autumn','winter']
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

# Convert a season to a Gregorian date
def season_to_gregorian(season):
  # Get the start of the season as a GregorianDate
  season_start = gregorian.GregorianDate(season.year,*seasons[season.season])
  season_start_jdn = gregorian.to_jdn(season_start)

  # Add the day number to the date
  jdn = season_start_jdn + season.day - 1

  # Return the value
  return gregorian.gregorian_from_jdn(jdn)

# Convert a season to a JDN
def season_to_jdn(season):

# Convert a Gregorian date to a season
def gregorian_to_season(date):
  # Assuming date is a GregorianDate tuple
  year, month, day = date

  # Return the value
  season = get_season(date)
  season_start = gregorian.GregorianDate(season[0],*seasons[season[1]])
  day = gregorian.difference(season_start,date) + 1
  return SeasonDate(*season,day)

# Convert a JDN to a season
def jdn_to_season(jdn):
  return gregorian_to_season(gregorian.jdn_to_gregorian(jdn))

# Season class
@total_ordering
class Season:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.year, self.season, self.day = jdn_to_season(jdn)

  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)

  # Format a Season date
  def format(self):
    return "{}, {}{} day of {}".format(self.year,self.day,ordinal(self.day),str.capitalize(self.season))

  # Convert this season to a string
  def __str__(self):
    return self.format()
