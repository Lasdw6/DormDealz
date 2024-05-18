import { useState } from "react";



const LoginForm = ({}) => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("") 

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            email,
            password
        }
        const url = "https://127.0.0.1:5000/login"
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status != 201 && response !=200) {
            const data = await response.json()
            alert(data.message)
        } else {
            //success
        }
    }
    return (
        <form>
            <div>
                <label htmlFor="email">Email:</label>
                <input 
                    type="text" 
                    id="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input 
                    type="text" 
                    id="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <button type="submit">Login</button>
        </form>    
    );
};

export default LoginForm