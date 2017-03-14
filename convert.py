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

# Generate CSV header
def genHeader(Target):
  Target.writerow(mappings.keys())

# Create a row with relative static values
def getSectionColumns(lines):
  row = copy.copy(mappings)
  for index, line in enumerate(lines):
    if line.startswith('MIZ'):
      row['Location'] = lines[index + 1]
      str = lines[index + 2]
      row['Lat'] = str[0:str.find('N')].strip()
      row['Long'] = str[str.find('N') + 1:str.find('W')].strip()
      row['Elevation'] = str[str.find('ELEV.') + 5:str.find('FT')].strip()
      row['TimeAt'] = lines[index + 3]
  return row

# Create rows from columns
def col2Rows(lines, row):
  rows = []
  for line in lines:
    rows.append(line)
  return rows

# Split sections by $$
lines = []
def splitSections(line, file):
  global lines
  if line.startswith('$$'):
    section = copy.copy(lines)
    lines = []  # clean section lines
    row = getSectionColumns(section)
    rows = col2Rows(section, row)
    file.writerow(row.values())
  else:
    lines.append(line)

# ============== Main =================
Source = open("201503022004.txt", "r")
with open("data.csv", "w") as f:
  Target = csv.writer(f)
  genHeader(Target)
  for line in Source:
    line = line.strip('\r\n')
    splitSections(line, Target)

# Show done
print 'generate csv done!'