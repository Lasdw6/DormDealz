import { useState, useEffect } from 'react'
import './App.css'
import ListingsList from './ListingsList'
function App() {
  const [titles, setTitles] = useState([])

  useEffect(() => {
    fetchListings()
  }, [])

  const fetchListings = async () => {
    const response = await fetch("https://http://127.0.0.1:5000/listings")
    const data = await response.json()
    setTitles(data.titles)
  }
  return <ListingsList titles={titles} />
}

export default App
