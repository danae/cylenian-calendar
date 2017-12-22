import collections
from functools import total_ordering
import cylenian
import gregorian
import season

# The names of the Cylenian months
month_names = [
  "Elsy'ondleð", "Nae Boryeð", "Seniðin", 
  "Liðin Boryeð", "Emmiðiða", "Omilnin", 
  "Karðondleð", "Seðaneðr", "Liliðin", 
  "Liðin Maroo", "Fðileð", "Elseniðor", 
  "Naeð Molið"
]
     
# Date class
@total_ordering
class Date:
  # Constructor
  def __init__(self, jdn):
    self.jdn = jdn
    self.cylenian_date = cylenian.from_jdn(self.jdn)
    self.gregorian_date = gregorian.from_jdn(self.jdn)
    
  # Comparison operators
  def __eq__(self, other):
    return self.jdn == other.jdn
  def __lt__(self, other):
    return self.jdn < other.jdn
  def __hash__(self):
    return hash(self.jdn)
    
  # Format this date in the two common notations
  def format_short(self):
    return ".".join([str(t) for t in self.cylenian_date])
  def format_long(self):
    return "{1} {0.day}, {0.era}E{0.year}".format(self.cylenian_date,month_names[self.cylenian_tuple.month - 1])
  
  # Convert to string
  def __str__(self):
    return self.format_long()
    
  # Return a date based on days since the Cylenian epoch
  @classmethod
  def from_days_since_epoch(cls, edn):
    return cls(cylenian.epoch + edn)
    
  # Return a date representing this Cylenian date
  @classmethod
  def from_cylenian(cls, date):
    return cls(cylenian.to_jdn(date))
    
  # Return a date representing this Gregorian date
  @classmethod
  def from_gregorian(cls, date):
    return cls(gregorian.to_jdn(date))
    
# Main function
if __name__ == "__main__":
  d = Date.from_gregorian((2017,12,22))
  print("jdn =",d.jdn)
  print(d.gregorian_date)
  print(d.cylenian_date)

