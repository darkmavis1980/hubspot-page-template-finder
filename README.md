# CSV Parser for HubSpot pages

This program reads a list of IDs from a CSV file, and then query the API to analyze which templates they use, and it creates a report.txt file with the resulting templates.

## Requirements

- Python 3.8
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

## Installation

To install dependencies, run `pipenv install`.

## Run it

Once you cloned the repository, installed the dependencies, simply run as following:

```shell
pipenv shell

python . csv/YOURFILE.CSV

# If you want to add a custom prefix name to the report add --name
python . csv/YOURFILE.CSV --name="CustomReport"
# Will generate report/CustomReport-30-06-2020-13-03-04.txt

```

Once finished, you will find the report file in the `reports` folder.