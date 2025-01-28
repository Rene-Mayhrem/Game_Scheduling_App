import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const [accessToken, setAccessToken] = useState('');

  useEffect(() => {
    // Check if there's an access token in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('access_token');
    if (token) {
      setAccessToken(token);
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const handleLogin = async () => {
    try {
      const response = await axios.get('http://backend:5000/login');
      const { auth_url } = response.data;
      window.location.href = auth_url;
    } catch (err) {
      console.error(err);
      setError('Failed to initiate login');
    }
  };

  const handleSearch = async () => {
    if (!accessToken) {
      setError('Please log in first');
      return;
    }

    try {
      const response = await axios.get('http://backend:5000/search', {
        params: { q: query },
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setResults(response.data.tracks.items);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to fetch results');
      setResults([]);
    }
  };

  return (
    <div className="App">
      <h1>Spotify Search</h1>
      {!accessToken ? (
        <button onClick={handleLogin}>Log in with Spotify</button>
      ) : (
        <>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for tracks..."
          />
          <button onClick={handleSearch}>Search</button>
        </>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {results.map((track) => (
          <li key={track.id}>
            <img src={track.album.images[0].url} alt={track.name} width="100" />
            <div>
              <strong>{track.name}</strong> by {track.artists[0].name}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;