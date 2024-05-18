import React from "react"

const ListingsList = ({titles}) => {
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
                {titles.map((titles) => (
                    <tr key={titles.id}>
                        <td>{titles.id}</td> 
                        <td>{titles.title}</td>
                    </tr>

                ))}    
            </tbody>   
        </table>           
    </div>
}

export default ListingsList