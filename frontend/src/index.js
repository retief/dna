import React, { useEffect, useState, useRef } from "react";
import { render } from "react-dom";
import regeneratorRuntime from "regenerator-runtime";
import Cookies from 'js-cookie';

const csrftoken = Cookies.get('csrftoken');

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

function SearchBox(props) {
    const [query, setQuery] = useState("");
    const search = () => {
        props.runSearch(query);
    };
    const onChange = (event) => {
        setQuery(event.target.value);
    }
    return (<div>
        <input type="text" value={query} onChange={onChange} />
        <input type="submit" value="Search" onClick={search} />
    </div>);
}

function SearchResult(props) {
    const search = props.search;
    if (search.genome === "") {
        return <div>{search.query}:</div>
    }
    return (<div>
        {search.query}: in genome {search.genome} at location {search.location} within protein {search.protein_id} at location {search.feature_location}
    </div>)
}

function App() {
    const [searches, setSearches] = useState(null);

    const getResults = async () => {
        const response = await fetch("/api/results");
        const json = await response.json();
        setSearches(json.results);
    }

    const runSearch = async (query) => {
        await fetch("/api/search", {
            method: "POST",
            body: JSON.stringify({query: query}),
            headers: {'X-CSRFToken': csrftoken},
        });
        await getResults();
        console.log("gotten results");
    }

    useEffect(getResults, []);

    useInterval(getResults, 3000);

    if (searches === null) {
        return <div>Loading ...</div>
    }

    const results = searches.map((search) => <SearchResult search={search} key={search.id} />)

    return (<div>
        <SearchBox runSearch={runSearch} />
        <div>{results}</div>
    </div>);
}

const container = document.getElementById("app");
render(<App />, container);
