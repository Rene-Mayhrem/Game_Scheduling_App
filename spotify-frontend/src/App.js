import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://localhost:5000/search', {
        params: { q: query },
      });
      setResults(response.data.tracks.items);
      setError('');
    } catch (err) {
      setError('Failed to fetch results');
      setResults([]);
    }
  };

  return (
    <div className="App">
      <h1>Spotify Search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for tracks..."
      />
      <button onClick={handleSearch}>Search</button>

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