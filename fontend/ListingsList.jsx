import React from "react"
const ListingsList = ({listings}) => {
    /* return <div>
        <h2> Listings </h2> 
        <table>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Title</th>
                    <th>Desc</th>
                </tr>
            </thead> 
            <tbody>
                {listings.map((listings) => (
                    <tr key={listings.id}>
                        <td>{listings.id}</td> 
                        <td>{listings.title}</td>
                        <td>{listings.description}</td>
                    </tr>

                ))}    
            </tbody>   
        </table>           
    </div> 
   /* return (
    <div> 
        {listings.map((listings) => ( 
            <Card id={listings.id} title={listings.title} description={listings.description} /> 
        ))} 
    </div>) */
}

export default ListingsList