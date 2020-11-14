import React, { useEffect, useState, useRef } from "react";
import { render } from "react-dom";
import regeneratorRuntime from "regenerator-runtime";

function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

function App() {
    const [searches, setSearches] = useState([]);

    const getResults = async () => {
        const response = await fetch("/api/results");
        const json = await response.json();
        setSearches(json.results);
    }

    useEffect(getResults, []);

    useInterval(getResults, 3000);

    return <div>There are {searches.length} searches</div>;
}

const container = document.getElementById("app");
render(<App />, container);
