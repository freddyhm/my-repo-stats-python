import requests
import datetime
import pytz

from rest_framework.exceptions import NotFound, Throttled, APIException

from api.utilities.part_of_day import Part_Of_Day

class CommitFetcherService:
    def __init__(self, username, reponame, timezone):
        self.username = username
        self.reponame = reponame
        self.timezone = timezone

    def get_part_of_day(self, hour):
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

    def get_stats(self):

        commit_url = f"https://api.github.com/repos/{self.username}/{self.reponame}/commits?per_page=100"
        response = requests.get(commit_url)

        if response.status_code == 404:
            raise NotFound()
        elif response.status_code == 403:
            raise Throttled()
        elif response.status_code == 200:
            data = response.json()
            return self.format_raw_data(data)
        else:
            print(f"api exception with status_code: {response.status_code}")
            raise APIException()

    def format_raw_data(self, data):
        commit_hours = self.get_commit_hours(data)
        commits_by_part_of_day_count = self.group_commits_by_part_of_day_count(commit_hours)
        commits_by_part_of_day_percentage = self.group_commits_by_part_of_day_percentage(len(commit_hours), commits_by_part_of_day_count)

        return {
            "morning": commits_by_part_of_day_percentage.get(Part_Of_Day.MORNING, 0),
            "afternoon": commits_by_part_of_day_percentage.get(Part_Of_Day.AFTERNOON, 0),
            "evening": commits_by_part_of_day_percentage.get(Part_Of_Day.EVENING, 0),
            "night": commits_by_part_of_day_percentage.get(Part_Of_Day.NIGHT, 0)
        }

    def get_commit_hours(self, data):
        commit_hours = []

        for commit in data:
            date_string = commit["commit"]["author"]["date"]

            no_timezone_datetime = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            utc_datetime = pytz.timezone('UTC').localize(no_timezone_datetime)

            localized_hour = utc_datetime.astimezone(pytz.timezone(self.timezone)).hour

            commit_hours.append(localized_hour)

        return commit_hours

    def group_commits_by_part_of_day_percentage(self, total_commits, commits_by_part_of_day_count):
        commits_by_part_of_day_percentage = {}

        for part_of_day in commits_by_part_of_day_count:
            commits_by_part_of_day_percentage[part_of_day] = round(commits_by_part_of_day_count[part_of_day] / total_commits * 100, 2)

        return commits_by_part_of_day_percentage

    def group_commits_by_part_of_day_count(self, commit_hours):
        part_of_day_dict = {}
        for hour in commit_hours:
            part_of_day = self.get_part_of_day(hour)
            if part_of_day in part_of_day_dict:
                part_of_day_dict[part_of_day] += 1
            else:
                part_of_day_dict[part_of_day] = 1
        return part_of_day_dict