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
    api_url = "https://api.github.com/repos/freddyhm/my-repo-stats-python/commits?per_page=100"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        # get the hour of each commit and store it in a list
        hours = []
        for commit in data:
            date_string = commit["commit"]["author"]["date"]

            no_timezone_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            utc_datetime = pytz.timezone('UTC').localize(no_timezone_datetime)

            hour = utc_datetime.astimezone(pytz.timezone('US/Eastern')).hour

            hours.append(hour)
            

        # get dictionary where key is part of day and value is part of day percentage over total values
        part_of_day_dict = {}
        for hour in hours:
            part_of_day = get_part_of_day(hour)
            if part_of_day in part_of_day_dict:
                part_of_day_dict[part_of_day] += 1
            else:
                part_of_day_dict[part_of_day] = 1

        # replace count in dictionary with percentage
        total = len(hours)
        for part_of_day in part_of_day_dict:
            part_of_day_dict[part_of_day] = round(part_of_day_dict[part_of_day] / total * 100, 2)

        return part_of_day_dict
    else:
        print("Error: ", response.status_code)

