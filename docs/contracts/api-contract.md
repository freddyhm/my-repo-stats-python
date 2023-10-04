# API Contract

- Who can use the API?
- What they can do?
- How they do it?
- What they need to do it?
- What do they get in returned?

## API Canvas ##

| Who? | What? | How? | Input? | Output? | Goal |
| --- | --- | --- | --- | --- | --- |
| Visitors | Get statistics | Use pre-set buttons to get statistics (ex: time-based, day-based, etc.) | Github username, Github repository name, Repository timezone, Type of statistic | Selected statistic in raw form to be consumed by client | Get statistics via pre-set buttons |
| Admin (out-of-scope) |  - | - | - | - | - |

## API Contract

**v1.0**

- First version will only return part of the day percentage statistics for the last 100 commits.

# Stats

- Stats object

```
{
  type: string
  morning: float,
  afternoon: float,
  evening: float,
  night: float,
}
```

**GET /stats/:user_name/:repo_name/:timezone**

Returns all stats for the specified user name, repository name, and timezone

- **URL Params**

  _Required:_ `user_name=[string]`

  _Required:_ `repo_name=[string]`

  _Required:_ `timezone=[string] TZDB identifier`

- **Data Params**
  None
- **Headers**
  Content-Type: application/json
- **Success Response:**

  - **Code:** 200

    **Content:**

    ```
    {
    stats: [
            {<stats_object>}
            ]
    }
    ```

- **Error Response:**

  - **Code:** 404

    **Content:** `{ error : "Username and/or repo name do not exist in Github" }`

  - **Code:** 400

    **Content:** `{ error : "User name or repo name are not valid" }`

  - **Code:** 429

    **Content:** `{ error : "Too many requests sent to Github" }`

  - **Code:** 500

    **Content:** `{ error : "Could not fetch data from Github API" }`


## v2.0

- Users cannot modify or delete existing stat reports
- Stat reports provide content via `stat_content` field which will hold a JSON string
- Primary key (composite): username and reponame

### Ideas for further versions:

- Support different type of stats
- Support fetching different batch sizes for commits (default 100)

# StatReport

- StatReport object

```
{
  username: string,
  reponame: string,
  timezone: string,
  stat_content: string
	created_at: DateTime
}
```

**GET /stats/:user_name/:repo_name**

Returns all stats for the specified user name, repository name, and timezone

- **URL Params**

  _Required:_ `user_name=[string]`

  _Required:_ `repo_name=[string]`

- **Data Params**
  None
- **Headers**
  Content-Type: application/json
- **Success Response:**

  - **Code:** 200

    **Content:**

    ```
    {
      <stat_report_object>
    }
    ```

- **Error Response:**

  - **Code:** 404

    **Content:** `{ error : "Username and/or repo name do not exist in Github" }`

  - **Code:** 400

    **Content:** `{ error : "User name or repo name are not valid" }`

  - **Code:** 429

    **Content:** `{ error : "Too many requests sent to Github" }`

  - **Code:** 500

    **Content:** `{ error : "Could not fetch data from Github API" }`

**POST /stats/:user_name/:repo_name/:timezone**

Returns all stats for the specified user name, repository name, and timezone

- **URL Params**

  _Required:_ `user_name=[string]`

  _Required:_ `repo_name=[string]`

  _Required:_ `timezone=[string] TZDB identifier`

- **Data Params**
  None
- **Headers**
  Content-Type: application/json
- **Success Response:**

  - **Code:** 201 Created

    **Content:**

    ```
    {
			<stat_report_object>
    }
    ```

- **Error Response:**

  - **Code:** 409 Conflict

    **Content:** `{ error : "Report already exists for username and repo name" }`

  - **Code:** 400 Bad Request

    **Content:** `{ error : "User name, repo name, or timezone are not valid" }`

  - **Code:** 429 Too Many Requests

    **Content:** `{ error : "Too many requests sents" }`

  - **Code:** 503 Forbidden

    **Content:** `{ error : "Could not fetch data from Github API" }`

  - **Code:** 500 Internal Server Error

    **Content:** `{ error : "Unable to fetch or generate report" }`