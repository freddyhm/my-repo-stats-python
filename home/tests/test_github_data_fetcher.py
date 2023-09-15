import unittest
from parameterized import parameterized
from home.services.github_data_fetcher import get_github_commits
from home.services.github_data_fetcher import get_part_of_day
from home.services.github_data_fetcher import Part_Of_Day

class TestGithubDataFetcher(unittest.TestCase):

    def test_get_part_of_day_percentage_of_commits(self):
        commits = get_github_commits()
        assert isinstance(commits, dict)
        assert Part_Of_Day.MORNING in commits
        assert Part_Of_Day.AFTERNOON in commits
        assert Part_Of_Day.EVENING in commits
        assert Part_Of_Day.NIGHT in commits


    @parameterized.expand([
        (Part_Of_Day.MORNING, 0),
        (Part_Of_Day.MORNING, 5),
        (Part_Of_Day.AFTERNOON, 14),
        (Part_Of_Day.EVENING, 19),
        (Part_Of_Day.NIGHT, 23),
        (Part_Of_Day.INVALID_HOUR, -5)
    ])
    def test_get_part_of_day(self, expected_result, hour):
        result = get_part_of_day(hour)
        assert isinstance(result, Part_Of_Day)
        self.assertEqual(result, expected_result)
        
        