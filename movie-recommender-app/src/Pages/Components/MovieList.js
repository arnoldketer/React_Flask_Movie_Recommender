// MovieList.js
import React, { useEffect, useState } from 'react';
import './styles/MovieList.css';

const API_KEY = '94775c9ff6104080c8be090cca0b69ec';
const BASE_URL = 'https://api.themoviedb.org/3';

const MovieList = () => {
  const [latestMovies, setLatestMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [upcomingMovies, setUpcomingMovies] = useState([]);

  // Fetch function to get movies from TMDb API
  const fetchMovies = async (type, setter) => {
    try {
      const response = await fetch(`${BASE_URL}/movie/${type}?api_key=${API_KEY}`);
      const data = await response.json();
      setter(data.results.slice(0, 20)); // Limit to 5 movies per category
    } catch (error) {
      console.error(`Error fetching ${type} movies:`, error);
    }
  };

  useEffect(() => {
    fetchMovies('now_playing', setLatestMovies);
    fetchMovies('popular', setPopularMovies);
    fetchMovies('upcoming', setUpcomingMovies);
  }, []);

  const renderMovies = (movies) => (
    <div className="movie-row">
      {movies.map((movie) => (
        <div key={movie.id} className="movie-card">
          <img
            src={`https://image.tmdb.org/t/p/w200${movie.poster_path}`}
            alt={movie.title}
            className="movie-poster"
          />
          <h3 className="movie-title">{movie.title}</h3>
        </div>
      ))}
    </div>
  );

  return (
    <div className="movie-list">
      <h2>Latest Movies</h2>
      {renderMovies(latestMovies)}

      <h2>Most Popular Movies</h2>
      {renderMovies(popularMovies)}

      <h2>Upcoming Movies</h2>
      {renderMovies(upcomingMovies)}
    </div>
  );
};

export default MovieList;


