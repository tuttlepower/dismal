import "./App.css";
import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from './components/Home';
import About from './components/About';

export const light = {
  palette: {
    type: "light",
  },
};
export const dark = {
  palette: {
    type: "dark",
  },
};

function App() {
  return (
      <main>
          <Switch>
              <Route path="/" component={Home} exact />
              <Route path="/about" component={About} />
          </Switch>
      </main>
  )
}

export default App;
