import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [username, setUsername] = useState("test");
  const [repoName, setRepoName] = useState("ok");
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
      })
      .catch((error) => {});
  };

  return (
    <div className="App">
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
  );
}

export default App;
