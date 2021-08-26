import logo from './logo.svg';
import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import AlertDismissible from './AlertDismissible';
ReactDOM.render(<App />, document.getElementById('root'));


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <Button variant="primary">Primary</Button>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <AlertDismissible />
      </header>
    </div>
  );
}
export default App;
