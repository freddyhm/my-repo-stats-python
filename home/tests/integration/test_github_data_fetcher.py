import unittest
from home.services.github_data_fetcher import get_github_commits
from home.services.github_data_fetcher import Part_Of_Day

class TestGithubDataFetcher(unittest.TestCase):

    def test_get_part_of_day_percentage_of_commits(self):
        result = get_github_commits()
        assert isinstance(result, dict)
        assert Part_Of_Day.MORNING in result
        assert Part_Of_Day.AFTERNOON in result
        assert Part_Of_Day.EVENING in result
        assert Part_Of_Day.NIGHT in result
        