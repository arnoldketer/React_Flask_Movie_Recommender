// Movies.js
import React from 'react';
import MovieList from './Components/MovieList';
import NavBar from './Components/NavBar';
import Footer from './Components/Footer';

const Movies = () => {
  return (
    <div>
      <NavBar isHome={true} />
      <MovieList />
      <Footer />
    </div>
  );
};

export default Movies;

