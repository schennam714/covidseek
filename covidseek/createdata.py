import json
counties = []
for line in open('/Users/shreyas/Desktop/Web Dev/covidseek/covidseek/response.json', 'r'):
    counties.append(json.loads(line))