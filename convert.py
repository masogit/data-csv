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

columns = ['Temperature', 'WindSpeed', 'WindDirection', 'RelativeHumidity', 'DewPoint']

# Generate CSV header
def genHeader(file):
  file.writerow(mappings.keys())

# Generate CSV rows
def genRows(rows, file):
  for row in rows:
    file.writerow(row.values())

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

# Split columns from Col15
def arrayCol15(line, rows, rawRow, columnName):
  pos = 15
  index = 0
  while (len(line) > pos):
    if (len(rows) > index):
      row = rows[index]
      row[columnName] = line[pos:pos + 1]
    else:
      row = copy.copy(rawRow)
      row[columnName] = line[pos:pos + 1]
      rows.append(row)
    pos += 2
    index += 1

# Create rows from columns
def col2Rows(lines, row):
  rows = []
  for line in lines:
    for col in columns:
      if line.startswith(row[col]):
        arrayCol15(line, rows, row, col)
        break
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
    genRows(rows, file)
    # file.writerow(row.values())
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