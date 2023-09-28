import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const apiUrl = process.env.REACT_APP_API_URL;

  const [error, setError] = useState("");
  const [stat, setStat] = useState("");
  const [username, setUsername] = useState("freddyhm");
  const [repoName, setRepoName] = useState("my-repo-stats-python");
  const [selectedOption, setSelectedOption] = useState("America/Montreal");

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handleRepoNameChange = (e) => {
    setRepoName(e.target.value);
  };

  const handleSelectChange = (e) => {
    setSelectedOption(e.target.value);
  };

  function formatErrorMessage(error) {

    let message = "Unknown error: something went wrong";

    if (error.code === 'ERR_NETWORK') {
      message = "Error: Could not connect to the service :("
    } else if (error.response.status === 404 || error.response.status === 500) {
      message = "Error: " + error.response.data;
    } else if (error.response.status === 429) {
      message = "Error: Too many requests sent to Github, please try again in an hour!";
    }

    return message;
  }

  const getStats = () => {
    axios
      .get(
        `${apiUrl}/api/stats/username/${username}/repo/${repoName}/?timezone=${selectedOption}`
      )
      .then((response) => {
        setStat(response.data.stat_content);
      })
      .catch((error) => {
        let error_message = formatErrorMessage(error);
        setError(error_message);
      });
  };

  return (
    <div className="App">
      <br />
      <div>
        <p>
          Github.com/
          <input
            type="text"
            placeholder="enter username"
            value={username}
            onChange={handleUsernameChange}
          />
          /
          <input
            type="text"
            placeholder="enter repo name"
            value={repoName}
            onChange={handleRepoNameChange}
          />
        </p>
        <p>
          Timezone:
          <select value={selectedOption} onChange={handleSelectChange}>
            <option value="America/Montreal">America/Montreal</option>
            <option value="America/Vancouver"> America/Vancouver</option>
          </select>
        </p>
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
        <button onClick={getStats}>Get Stats</button>
      </div>
      <br />
      <div>
        <h2>When are commits typically made during the day?</h2>
        <br />
        <h3>Morning: {stat ? stat.morning : 0}%</h3>
        <br />
        <h3>Afternoon: {stat ? stat.afternoon : 0}%</h3>
        <br />
        <h3>Evening: {stat ? stat.evening : 0}%</h3>
        <br />
        <h3>Night: {stat ? stat.night : 0}%</h3>
      </div>
    </div>
  );
}

export default App;
