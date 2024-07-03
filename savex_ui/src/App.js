import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';

function App() {
  const [defaultValue, setDefaultValue] = useState(null);
  useEffect(() => {
    fetch('http://127.0.0.1:8000/default-values/')
      .then(response => response.json())
      .then(data => setDefaultValue(data.birth_year));
  }, []);
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>Welcome to the Retirement Portfolio page.</p>
        <div>
          <label>Select a date:</label>
          <input type="date" defaultValue={defaultValue} />
        </div>
      </header>
    </div>
  );
}

export default App;
