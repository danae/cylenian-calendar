'''
Valid parser grammar:

- Cylenian date
  {era}.{year}.{month}.{day}
  {month_name} {day}, {era}E{year}
  {day}th of {month_name} {era}E{year}
  today
  tomorrow
  yesterday
  next/last month
  next/last year
  next/last era
  leap era
  
- Gregorian date
  {year:04d}-{month:02d}-{day:02d}
  {year:04d}/{day:02d}/{month:02d}

- Season
  {year}, {day}th day of {season}
  {day}th day of {season} {year}
  start/end of next {season}
  start/end of last {season}
  current/next/last season
  
- Moon phases
  moon/moon phase/current moon phase
  next/last full moon
  next/last new moon
  next/last blue moon  
'''