import { useState } from 'react';
import './App.css';

import { SearchBar } from './components/SearchBar';

function App() {
  return (
    <div className='App'>
      <div ClassName="search-bar-container">
        <SearchBar />
        <div>SearchResults</div>
      </div>
    </div>
  );
}

export default App;
