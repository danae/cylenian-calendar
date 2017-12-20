# monthdays for the start of seasons
season_starts = {'winter': (12,21), 'spring': (3,21), 'summer': (6,21), 'autumn': (12,21)}

# Get the season for a Gregorian date
def get_season(date)
  # Assuming date is a tuple (year, month, day)
  monthday = (date[1],date[2])
  
  # Calculate the season
  if (monthday >= (12,21) and monthday <= (12,31)) or (monthday >= (1,1) and monthday < (3,21)):
    return "winter"
  elif monthday >= (3,21) and monthday < (6,21):
    return "spring"
  elif monthday >= (6,21) and monthday < (9,21):
    return "summer"
  elif monthday >= (9,21) and monthday < (12,21):
    return "autumn"

# Get the start of a season for a Gregorian date as a Gregorian tuple (year, month, day)
def start_of_season(date, season):
  # Get the year
  year = date[0]
  
  # Get the start of the season
  start = season_starts[season]
  if start is None:
    raise ValueError("The season {} is not a valid season; valid seasons are winter, spring, summer and autumn".format(season))
  
  # If the season is winter
  if season == 'winter':
    return (year - 1,start[0],start[1])
  else:
    return (year,start[0],start[1])
    
# Get the day of the season for a Gregorian date
def day_of_season(date):
  pass

# Season class
class season:
  
  # Constructor
  def __init__(self, month, day):
    self.season = calculate_season(month,day)
    