import collections
import datetime
from functools import total_ordering
import cylenian
import gregorian
import moon

# Date class
@total_ordering
class Date:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.cylenian_date = cylenian.CylenianDate(self.jdn)
    self.gregorian_date = gregorian.GregorianDate(self.jdn)
    self.moon = moon.Moon(self.jdn)

  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)

  # Convert to string
  def __str__(self):
    return self.cylenian_date.format_long()

  # Return a date representing this Cylenian date
  @classmethod
  def from_cylenian(cls, era, year, month, day):
    return cls(cylenian.cylenian_to_jdn(era,year,month,day))

  # Return a date representing this Gregorian date
  @classmethod
  def from_gregorian(cls, year, month, day):
    return cls(gregorian.gregorian_to_jdn(year,month,day))

  # Return a date representing today
  @classmethod
  def today(cls):
    today = datetime.date.today()
    return cls.from_gregorian(today.year,today.month,today.day)

# Main function
if __name__ == "__main__":
  date = Date.today()
  print(date.gregorian_date)
  print(date.cylenian_date)
  print(date.moon)
