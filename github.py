import requests

def get_github_commits():
    api_url = "https://api.github.com/repos/freddyhm/MyRepoStats/commits"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print("API Response: ", data)

        # format data in dictionary
        my_dict = dict(test=data) 

        return my_dict
    else:
        print("Error: ", response.status_code)