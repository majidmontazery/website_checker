import csv
import requests
from fake_useragent import UserAgent
from http import HTTPStatus

# Reads websites from a CSV file and returns them as a list
def get_websites(csv_path: str):
    websites: list[str] = []
    # Open the CSV file in read mode
    with open(csv_path,'r') as file:
      reader = csv.reader(file)
      for row in reader:
          # Check that the row has at least 2 columns
       if len(row) > 1:
          site = row[1] # Take the second column as the website
                # Add "https://" if it's missing
          if not site.startswith('https://'):
              site = f'https://{site}'
          websites.append(site)
      return websites

# Generates a fake User-Agent string (Chrome browser)
def get_user_agent():
    ua = UserAgent()
    return ua.chrome
# Returns a description for a given HTTP status code
def get_status_description(status_code: int):
    for value in HTTPStatus:
        # Example: (200 OK) Request fulfilled, document follows
        if value.value == status_code:
            return f'({value.value} {value.name}) {value.description}'
    # If the code is not recognized, return unknown
    return f'({status_code}) Unknown status code...'

def check_website(website: str, user_agent):
    try:
        response = requests.get(website, headers={'User-Agent': user_agent}, timeout=5)
        code: int = response.status_code
        print(website, get_status_description(code))
    except Exception as e:
        print(f'**Could not get information for website: "{website}" | Error: {e}')

def main():
    sites: list[str] = get_websites('websites.csv')
    user_agent = get_user_agent()

    for site in sites:
        check_website(site, user_agent)

if __name__ == '__main__':
    main()