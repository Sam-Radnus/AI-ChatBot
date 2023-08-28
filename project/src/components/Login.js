import React from 'react'
import { useState,useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  AwesomeButton,
  AwesomeButtonProgress,
  AwesomeButtonSocial,
} from 'react-awesome-button';
const Login = () => {
  const[email,setEmail]=useState('');
  const[password,setPassword]=useState('');
  const navigate=useNavigate();
   const ValidateToken=()=>{
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/Chat');
    }
  };


  useEffect(() => {
    ValidateToken();
  }, [])
  const login = async (email, password) => {

    try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username:email, password:password }),
        });
        console.log(response);
        const data = await response.json();
        console.log(data);
        if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            alert("Logged in successfully!");
            const userInfo={
              'username':data.email,
              'password':data.password,
            }

            localStorage.setItem('userInfo',JSON.stringify(userInfo));
            navigate('/Chat');
            // Redirect to dashboard or other page if needed
        } else {
            console.error("Error logging in:", data.error);
            alert("error logging in:", data.error);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
};

  return (
    <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: '400px', height: '395px' }}>
       
        <h1 style={{textAlign:"center"}}>Sign In</h1>
        <div className="form-outline mb-4">
          <label className="form-label" for="form2Example1">Username</label>
          <input type="text" value={email}  onChange={(e)=>{
                setEmail(e.target.value); 
          }}id="form2Example1" className="form-control" />

        </div>


        <div className="form-outline mb-4">
          <label className="form-label" for="form2Example2">Password</label>
          <input type="password" value={password}  onChange={(e)=>{
                setPassword(e.target.value); 
          }} id="form2Example2" className="form-control" />

        </div>


      

 <div style={{display:'flex',justifyContent:'center',alignItems:'center'}} className="row mb-4">
                <span style={{marginLeft:'50%'}} type="button" onClick={()=>{
                    login(email,password);
                }}> <AwesomeButton
                size="large"
                type="primary"
              >
                Sign-In
              </AwesomeButton></span>
        </div>

        <div className="text-center">
          <p>Not a member?<Link to="/signup">Sign-Up</Link></p>

        </div>
    
    </div>
  )
}

export default Login