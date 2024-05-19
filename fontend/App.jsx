import { useState, useEffect } from 'react'
import './App.css'
import ListingsList from './ListingsList'
import LoginForm from './Login'
import Card from './Card'

function App() {
  const [listings, setListings] = useState([])

  useEffect(() => {
    console.log("AAAvA")
    fetchListings()
  }, [])

  const fetchListings = async () => {
    const response = await fetch("http://127.0.0.1:5000/listings")
    const data = await response.json()
    console.log("AAA")
    console.log(data.listings)
    setListings(data.listings)
    console.log(data.listings)
  }
  return (
  <>
    <Card listings={listings} />
  </>
  );
}

export default App
