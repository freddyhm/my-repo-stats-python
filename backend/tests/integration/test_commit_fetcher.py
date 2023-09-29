import unittest
from api.services.commit_fetcher_service import CommitFetcherService

class TestCommitFetcher(unittest.TestCase):

    def test_get_part_of_day_percentage_of_commits(self):
        commit_fetcher_service = CommitFetcherService("freddyhm", "my-repo-stats-python", "America/Montreal")
        result = commit_fetcher_service.get_stats()
        assert isinstance(result, dict)
        assert "morning" in result
        assert "afternoon" in result
        assert "evening" in result
        assert "night" in result
        