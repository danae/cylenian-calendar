import collections
from functools import total_ordering
import cylenian
import gregorian
import season
     
# Date class
@total_ordering
class Date:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.days_since_epoch = self.jdn - cylenian.epoch
    self.cylenian_date = cylenian.from_jdn(self.jdn)
    self.gregorian_date = gregorian.from_jdn(self.jdn)
    self.season_date = season.from_gregorian(self.gregorian_date)
    
  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)
    
  # Format this date
  def format_cylenian(self):
    return cylenian.format(self.cylenian_date)
  def format_cylenian_long(self):
    return cylenian.format_long(self.cylenian_date)
  def format_gregorian(self):
    return gregorian.format(self.gregorian_date)
  def format_season(self):
    return season.format(self.season_date)
  
  # Convert to string
  def __str__(self):
    return self.format_long()
    
  # Return a date based on days since the Cylenian epoch
  @classmethod
  def from_days_since_epoch(cls, days_since_epoch):
    return cls(cylenian.epoch + days_since_epoch)
    
  # Return a date representing this Cylenian date
  @classmethod
  def from_cylenian(cls, date):
    return cls(cylenian.to_jdn(date))
    
  # Return a date representing this Gregorian date
  @classmethod
  def from_gregorian(cls, date):
    return cls(gregorian.to_jdn(date))
    
  # Return a date representing this season date
  @classmethod
  def from_season(cls, date):
    return cls.from_gregorian(season.to_gregorian(date))

# Main function
if __name__ == "__main__":
  dates = [(2017,1,5),(2017,3,21),(2017,3,31),(2017,8,20),(2017,12,22)]
  for date in dates:
    date = Date.from_gregorian(date)
    print(date.format_gregorian())
    print(date.format_cylenian_long())
    print(date.format_season())
    print("-----")
