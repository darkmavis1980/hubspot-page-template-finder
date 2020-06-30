import configparser
import csv
import json
import requests

file = "csv/test.csv"

def getConfig():
    config = configparser.ConfigParser()
    try:
        config.read('./conf/conf.ini')
        return config
    except:
        raise Exception("Cannot read the configuration file")

def readCSV(file):
    """
    Reads a CSV file and returns the result rows
    """
    rows = []
    with open(file) as csvFile:
        csvRows = csv.reader(csvFile, delimiter=',', quotechar='"')
        headers = next(csvRows)
        for row in csvRows:
            rows.append(row)
    data = dict()
    data['rows'] = rows
    data['headers'] = headers
    return data

def getIds(rows, headers):
    """
    Parse the rows and returns an array with all the IDs
    """
    ids = []
    headers = [header.lower() for header in headers]
    index = headers.index("id")
    for row in rows:
        ids.append(row[index])
    return ids

def parseCSV(file):
    """
    Get the rows from the passed CSV file, then it does a request for each ID and parses the body response to find for templates
    """
    config = getConfig()
    hapikey = config.get('HUBSPOT', 'HAPIKEY')
    api_url_base = config.get('HUBSPOT', 'API_URL')
    csvData = readCSV(file)
    headers = csvData["headers"]
    csvRows = csvData["rows"]
    ids = getIds(csvRows, headers)
    templates = []
    for id in ids:
        api_url = api_url_base.format(id, hapikey)
        response = requests.get(api_url)
        print("Fetching Page ID: {}".format(id))
        if response.status_code == 200:
            body = json.loads(response.content.decode('utf-8'))
            if body["template_path"] not in templates:
                templates.append(body["template_path"])
                print("Found new template: {}".format(body["template_path"]))
        else:
            print("Error: Couldn't fetch page ID: {}".format(id))
            pass

    with open("report.txt", "w+") as reportFile:
        for t in templates:
            reportFile.write("{}\n".format(t))

if __name__ == "__main__":
    parseCSV(file)