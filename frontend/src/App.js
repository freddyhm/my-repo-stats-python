import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
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

  const getStats = () => {
    axios
      .get(
        `http://localhost:8000/api/stats/username/${username}/repo/${repoName}/?timezone=${selectedOption}`
      )
      .then((response) => {
        console.log(response);
        setStat(response.data);
      })
      .catch((error) => {
        console.log(error);
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
