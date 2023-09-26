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

def get_part_of_day_percentage_of_commits():
    response = requests.get("https://api.github.com/repos/freddyhm/my-repo-stats-python/commits?per_page=100")

    if response.status_code == 200:
        data = response.json()
        return format_raw_data(data)
    else:
        print("Error: ", response.status_code)

def format_raw_data(data):
    commit_hours = get_commit_hours(data)
    commits_by_part_of_day_count = group_commits_by_part_of_day_count(commit_hours)
    commits_by_part_of_day_percentage = group_commits_by_part_of_day_percentage(len(commit_hours), commits_by_part_of_day_count)
    return commits_by_part_of_day_percentage

def get_commit_hours(data):
    commit_hours = []

    for commit in data:
        date_string = commit["commit"]["author"]["date"]

        no_timezone_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        utc_datetime = pytz.timezone('UTC').localize(no_timezone_datetime)

        localized_hour = utc_datetime.astimezone(pytz.timezone('US/Eastern')).hour

        commit_hours.append(localized_hour)

    return commit_hours

def group_commits_by_part_of_day_percentage(total_commits, commits_by_part_of_day_count):
    commits_by_part_of_day_percentage = {}

    for part_of_day in commits_by_part_of_day_count:
        commits_by_part_of_day_percentage[part_of_day] = round(commits_by_part_of_day_count[part_of_day] / total_commits * 100, 2)

    return commits_by_part_of_day_percentage

def group_commits_by_part_of_day_count(commit_hours):
    part_of_day_dict = {}
    for hour in commit_hours:
        part_of_day = get_part_of_day(hour)
        if part_of_day in part_of_day_dict:
            part_of_day_dict[part_of_day] += 1
        else:
            part_of_day_dict[part_of_day] = 1
    return part_of_day_dict

