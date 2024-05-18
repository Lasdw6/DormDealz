import React from "react"

const ListingsList = ({listings}) => {
    return <div>
        <h2> Listings </h2> 
        <table>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Title</th>
                </tr>
            </thead> 
            <tbody>
                {listings.map((listings) => (
                    <tr key={listings.id}>
                        <td>{listings.id}</td> 
                        <td>{listings.title}</td>
                    </tr>

                ))}    
            </tbody>   
        </table>           
    </div>
}

export default ListingsList