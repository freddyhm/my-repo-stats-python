import unittest
from home.services.commit_fetcher import get_part_of_day_percentage_of_commits
from home.services.commit_fetcher import Part_Of_Day

class TestCommitFetcher(unittest.TestCase):

    def test_get_part_of_day_percentage_of_commits(self):
        result = get_part_of_day_percentage_of_commits()
        assert isinstance(result, dict)
        assert Part_Of_Day.MORNING in result
        assert Part_Of_Day.AFTERNOON in result
        assert Part_Of_Day.EVENING in result
        assert Part_Of_Day.NIGHT in result
        