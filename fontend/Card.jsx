import React from "react";

const Card = ({listings}) => {
    return(
        <div>
            {listings.map((listings) => (
            <div className="card" key={listings.id}>
                <h2>{listings.title}</h2>
                <p>{listings.description}</p>
            </div>
            ))}       
        </div>
    );
}

export default Card