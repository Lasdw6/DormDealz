import { useState, useEffect } from 'react'
import './App.css'
import ListingsList from './ListingsList'
import LoginForm from './Login'
function App() {
  const [listings, setListings] = useState([])

  useEffect(() => {
    console.log("A")
    fetchListings()
  }, [])

  const fetchListings = async () => {
    const response = await fetch("http://127.0.0.1:5000/listings")
    const data = await response.json()
    console.log(data.listings)
    setListings(data.listings)
    console.log(data.listings)
  }
  return (
  <>
    <ListingsList listings={listings} />
    <LoginForm />
  </>
  );
}

export default App
