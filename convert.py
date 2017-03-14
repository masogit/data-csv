# TimeAt: Timestap at which forecast was made
# TimeFor: Timestamp for which the forecast was made
# Location: Weather station
# Lat,
# Long,
# Elevation,
# Temperature
# ForecastType
# WindSpeed
# WindDirection
# RelativeHumidity
# DewPoint
import csv

mappings = {
  'TimeAt': 'function',
  'TimeFor': 'DATE',
  'Location': 'function',
  'Lat': 'xx.xxN',
  'Long': 'xx.xxW',
  'Elevation': 'ELEV',
  'Temperature': 'TEMP',
  'ForecastType': 'XXXX',
  'WindSpeed': 'WIND SPD',
  'WindDirection': 'WIND SPD',
  'RelativeHumidity': 'RH',
  'DewPoint': 'DEWPT'
}

def genHeader(Target):
  Target.writerow(mappings.keys())

counter = 1
def genRow(line, Target):
  if line.startswith('$$'):
    global counter
    counter = counter + 1
    Target.writerow(['--', counter])

Source = open("201503022004.txt", "r")
with open("data.csv", "w") as f:
  Target = csv.writer(f)
  genHeader(Target)
  for line in Source:
    genRow(line, Target)

print 'generate csv done!'