import { useState, useEffect } from 'react'
import './App.css'
import ListingsList from './ListingsList'
function App() {
  const [listings, setListings] = useState([])

  useEffect(() => {
    console.log("A")
    fetchListings()
  }, [])

  const fetchListings = async () => {
    const response = await fetch("https://http://127.0.0.1:5000/listings")
    const data = await response.json()
    setListings(data.listings)
    console.log(data.listings)
  }
  return <ListingsList listings={listings} />
}

export default App
