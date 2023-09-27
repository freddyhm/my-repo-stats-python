import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [repoName, setRepoName] = useState("");

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handleRepoNameChange = (e) => {
    setRepoName(e.target.value);
  };

  const getStats = () => {
    axios
      .get(
        `http://localhost:8000/api/stats/username/${username}/repo/${repoName}/`
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
      <button onClick={getStats}>Get Stats</button>
    </div>
  );
}

export default App;
