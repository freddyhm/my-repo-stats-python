import requests
import enum
import datetime
import pytz

class Part_Of_Day(enum.Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4
    INVALID_HOUR = 5

def get_part_of_day(hour):

    is_morning = hour >= 0 and hour <= 11
    is_afternoon = hour >= 12 and hour <= 17
    is_evening = hour >= 18 and hour <= 20
    is_night = hour >= 21 and hour <= 23

    if is_morning:
        return Part_Of_Day.MORNING
    elif is_afternoon:
        return Part_Of_Day.AFTERNOON
    elif is_evening:
        return Part_Of_Day.EVENING 
    elif is_night:
        return Part_Of_Day.NIGHT
    else:
        return Part_Of_Day.INVALID_HOUR

def get_github_commits():
    api_url = "https://api.github.com/repos/freddyhm/MyRepoStats/commits"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print("API Response: ", data)

        # get the hour of each commit and store it in a list
        hours = []
        for commit in data:
            utc_date_string = commit["commit"]["author"]["date"]

            utc_datetime = datetime.datetime.strptime(utc_date_string, "%Y-%m-%dT%H:%M:%SZ")

            timezone = pytz.timezone("US/Eastern")
            hour = utc_datetime.astimezone(timezone).hour

            

        # format data in dictionary
        my_dict = dict(test=data) 

        return my_dict
    else:
        print("Error: ", response.status_code)

