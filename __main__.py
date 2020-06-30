import argparse
import configparser
import csv
from datetime import datetime
import json
import requests
import os

def get_config():
    config = configparser.ConfigParser()
    try:
        config.read('./conf/conf.ini')
        return config
    except:
        raise Exception("Cannot read the configuration file")

def read_csv(file):
    """
    Reads a CSV file and returns the result rows
    """
    rows = []
    with open(file) as csv_file:
        csv_rows = csv.reader(csv_file, delimiter=',', quotechar='"')
        headers = next(csv_rows)
        for row in csv_rows:
            rows.append(row)
    data = dict()
    data['rows'] = rows
    data['headers'] = headers
    return data

def get_ids(rows, headers):
    """
    Parse the rows and returns an array with all the IDs
    """
    ids = []
    headers = [header.lower() for header in headers]
    index = headers.index("id")
    for row in rows:
        ids.append(row[index])
    return ids

def parse_csv(file, report_name = None):
    """
    Get the rows from the passed CSV file, then it does a request for each ID and parses the body response to find for templates
    """
    config = get_config()
    hapikey = config.get('HUBSPOT', 'HAPIKEY')
    api_url_base = config.get('HUBSPOT', 'API_URL')
    csv_data = read_csv(file)
    headers = csv_data["headers"]
    csv_rows = csv_data["rows"]
    ids = get_ids(csv_rows, headers)
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

    current_date = datetime.today()
    current_date = current_date.strftime("%d-%m-%Y-%H-%M-%S")
    src_filename = os.path.splitext(os.path.basename(file))[0]
    filename = "reports/{}-{}.txt".format(src_filename, current_date)
    if report_name:
        filename = "reports/{}-{}.txt".format(report_name, current_date)
    with open(filename, "w+") as report_file:
        for t in templates:
            report_file.write("{}\n".format(t))

def init():
    """
    Init the CLI with the arguments and start the parsing process
    """
    parser = argparse.ArgumentParser(description='Parse a CSV file to find HubSpot pages templates')
    parser.add_argument('file', metavar='FILE', help='The file to parse')
    parser.add_argument('-n', '--name', help='Set a name for the report')
    args = parser.parse_args()
    if args.file:
        parse_csv(args.file, args.name)

if __name__ == "__main__":
    init()