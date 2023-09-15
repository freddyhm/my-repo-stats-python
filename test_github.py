import unittest
from github import get_github_commits

class TestGithub(unittest.TestCase):

    def test_get_part_of_day_percentage_of_commits(self):
        commits = get_github_commits()
        assert isinstance(commits, dict)