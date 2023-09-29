import unittest
from parameterized import parameterized
from unittest.mock import patch
from api.services.commit_fetcher_service import CommitFetcherService
from api.utilities.part_of_day import Part_Of_Day

class TestCommitFetcherService(unittest.TestCase):
    def setUp(self):
        self.username = "testuser"
        self.reponame = "testrepo"
        self.timezone = "America/New_York"
        self.service = CommitFetcherService(self.username, self.reponame, self.timezone)


    @parameterized.expand([
        (Part_Of_Day.MORNING, 0),
        (Part_Of_Day.MORNING, 5),
        (Part_Of_Day.AFTERNOON, 14),
        (Part_Of_Day.EVENING, 19),
        (Part_Of_Day.NIGHT, 23),
        (Part_Of_Day.INVALID_HOUR, -5)
    ])
    def test_get_part_of_day(self, expected_result, hour):
        # Arrange
        result = self.service.get_part_of_day(hour)

        # Act
        assert isinstance(result, Part_Of_Day)

        # Assert
        self.assertEqual(result, expected_result)

    @patch("api.services.commit_fetcher_service.requests.get")
    def test_get_stats_successful(self, mock_get):
        # Arrange
        response_data = [
            {"commit": {"author": {"date": "2023-09-28T10:00:00Z"}}}, # in EST -> 6am
            {"commit": {"author": {"date": "2023-09-28T15:30:00Z"}}}, # in EST -> 11:30am
            {"commit": {"author": {"date": "2023-09-28T19:45:00Z"}}}, # in EST -> 3:45pm
            {"commit": {"author": {"date": "2023-09-28T22:30:00Z"}}}, # in EST -> 6:30pm
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_data

        # Act
        result = self.service.get_stats()

        # Assert
        self.assertEqual(result, {
            "morning": 50.0,
            "afternoon": 25.0,
            "evening": 25.0,
            "night": 0
        })

if __name__ == '__main__':
    unittest.main()
