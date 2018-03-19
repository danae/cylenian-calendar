import bisect
import math

# 1980 January 0.0 in JDN
epoch = 2444238.5
# Ecliptic longitude of the Sun at epoch 1980.0
ecliptic_longitude_epoch = 278.833540
# Ecliptic longitude of the Sun at perigee
ecliptic_longitude_perigee = 282.596403
# Eccentricity of Earth's orbit
eccentricity = 0.016718
# Semi-major axis of Earth's orbit, in kilometers
sun_smaxis = 1.49585e8
# Sun's angular size, in degrees, at semi-major axis distance
sun_angular_size_smaxis = 0.533128
# Moon's mean longitude at the epoch
moon_mean_longitude_epoch = 64.975464
# Mean longitude of the perigee at the epoch
moon_mean_perigee_epoch = 349.383063
# Inclination of the Moon's orbit
moon_inclination = 5.145396
# Eccentricity of the Moon's orbit
moon_eccentricity = 0.054900
# Moon's angular size at distance a from Earth
moon_angular_size = 0.5181
# Semi-mojor axis of the Moon's orbit, in kilometers
moon_smaxis = 384401.0
# Parallax at a distance a from Earth
moon_parallax = 0.9507
# Synodic month (new Moon to new Moon), in days
synodic_month = 29.53058868
# Base date for E. W. Brown's numbered series of lunations (1923 January 16)
lunations_base = 2423436.0
# Properties of the Earth
earth_radius = 6378.16

# Precision used when describing the moon's phase in textual format,
# in phase_string().
PRECISION = 0.05
NEW =   0 / 4.0
FIRST = 1 / 4.0
FULL = 2 / 4.0
LAST = 3 / 4.0
NEXTNEW = 4 / 4.0

def phase_string(p):
  phase_strings = (
    (NEW + PRECISION, "New moon"),
    (FIRST - PRECISION, "Waxing crescent"),
    (FIRST + PRECISION, "First quarter"),
    (FULL - PRECISION, "Waxing gibbous"),
    (FULL + PRECISION, "Full moon"),
    (LAST - PRECISION, "Waning gibbous"),
    (LAST + PRECISION, "Last quarter"),
    (NEXTNEW - PRECISION, "Waning crescent"),
    (NEXTNEW + PRECISION, "New moon"))
  i = bisect.bisect([a[0] for a in phase_strings], p)
  return phase_strings[i][1]

# Calculate trigoniometric functions of a value in degrees
def dsin(d):
  return math.sin(math.radians(d))
def dcos(d):
  return math.cos(math.radians(d))

# Fixes an angle in degrees between 0 and 359
def fixangle(a):
  return a - 360.0 * (math.floor(a / 360.0))

# Solves the Kepler equation
def kepler(m):
  epsilon = 1e-6

  m = math.radians(m)
  e = m
  while True:
    delta = e - eccentricity * math.sin(e) - m
    e -= delta / (1.0 - eccentricity * math.cos(e))
    if abs(delta) <= epsilon:
      break

  return e

# Moon class
class Moon:
  # Constructor
  def __init__(self, jdn):
    day = jdn - epoch

    # Calculation of the Sun's position
    sun_mean_anomaly = fixangle((360.0 / 365.2422) * day)
    sun_perigree_coordinates_to_epoch = fixangle(sun_mean_anomaly + ecliptic_longitude_epoch - ecliptic_longitude_perigee)
    sun_eccent = kepler(sun_perigree_coordinates_to_epoch)
    sun_eccent = math.sqrt((1.0 + eccentricity) / (1.0 - eccentricity)) * math.tan(sun_eccent / 2.0)
    sun_eccent = 2.0 * math.degrees(math.atan(sun_eccent))
    sun_geocentric_elong = fixangle(sun_eccent + ecliptic_longitude_perigee)

    # Calculation of the Sun's distance
    sun_dist_factor = ((1 + eccentricity * dcos(sun_eccent)) / (1 - eccentricity**2))
    sun_dist = sun_smaxis / sun_dist_factor
    sun_angular_diameter = sun_dist_factor * sun_angular_size_smaxis

    # Calculation of the Moon's position
    moon_mean_longitude = fixangle(13.1763966 * day + moon_mean_longitude_epoch)
    moon_mean_anomaly = fixangle(moon_mean_longitude - 0.1114041 * day - moon_mean_perigee_epoch)
    moon_evection = 1.2739 * dsin(2.0 * (moon_mean_longitude - sun_geocentric_elong) - moon_mean_anomaly)
    moon_annual_equation = 0.1858 * dsin(sun_perigree_coordinates_to_epoch)
    moon_correction_term1 = 0.37 * dsin(sun_perigree_coordinates_to_epoch)
    moon_corrected_anomaly = moon_mean_anomaly + moon_evection - moon_annual_equation - moon_correction_term1
    moon_correction_equation_of_center = 6.2886 * dsin(moon_corrected_anomaly)
    moon_correction_term2 = 0.214 * dsin(2.0 * moon_corrected_anomaly)
    moon_corrected_longitude = moon_mean_longitude + moon_evection + moon_correction_equation_of_center - moon_annual_equation + moon_correction_term2
    moon_variation = 0.6583 * dsin(2.0 * (moon_corrected_longitude - sun_geocentric_elong))
    moon_present_longitude = moon_corrected_longitude + moon_variation

    # Calculation of the phase of the Moon
    moon_present_age = moon_present_longitude - sun_geocentric_elong
    moon_present_phase = (1.0 - dcos(moon_present_age)) / 2.0

    # Calculate distance of Moon from the center of the Earth
    moon_dist = (moon_smaxis * (1 - moon_eccentricity ** 2)) / (1 + moon_eccentricity * dcos(moon_corrected_anomaly + moon_correction_equation_of_center))

    # Calculate Moon's angular diameter
    moon_diam_frac = moon_dist / moon_smaxis
    moon_angular_diameter = moon_angular_size / moon_diam_frac

    # Set the result
    self.phase = phase_string(fixangle(moon_present_age) / 360.0)
    self.illumination = moon_present_phase
    self.age = synodic_month * fixangle(moon_present_age) / 360.0
    self.distance = moon_dist
    self.angle = moon_angular_diameter
    self.sun_distance = sun_dist
    self.sun_angle = sun_angular_diameter

  # Format an illumination
  def format(self):
    return 'Moon:\n' \
      + '- Phase: {}\n'.format(self.phase) \
      + '- Illumination: {:.1f}%\n'.format(self.illumination * 100.0) \
      + '- Moon Age: {:.2f}\n'.format(self.age) \
      + '- Moon Angle: {:.2f}\n'.format(self.angle) \
      + '- Moon Distance: {:.0f} km\n'.format(self.distance) \
      + '- Sun Angle: {:.2f}\n'.format(self.sun_angle) \
      + '- Sun Distance: {:.0f} km'.format(self.sun_distance)
