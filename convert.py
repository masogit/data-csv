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
import copy

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

def getSectionColumns(lines, file):
  row = copy.copy(mappings)
  for index, line in enumerate(lines):
    if line.startswith('MIZ'):
      row['Location'] = lines[index + 1]
      geoLine = lines[index + 2]
      row['Lat'] = geoLine[0:5]
      row['TimeAt'] = lines[index + 3]
  file.writerow(row.values())

sections = [[]]
def splitSections(line, file):
  lines = sections[len(sections) - 1]
  if line.startswith('$$'):
    getSectionColumns(lines, file)
  else:
    lines.append(line)


Source = open("201503022004.txt", "r")
with open("data.csv", "w") as f:
  Target = csv.writer(f)
  genHeader(Target)
  for line in Source:
    line = line.strip('\r\n')
    splitSections(line, Target)

# print sections
print 'generate csv done!'