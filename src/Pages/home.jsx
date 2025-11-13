import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import '../App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import Title from "../components/Title"

export function Home() {

  const [numSims, setNumSims] = useState(100000);
  const [bankroll, setBankroll] = useState(250000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  return (
    <>
    <body> 
        <div><Title></Title></div>
        <div class = "limitLink"> 
            <Link to="/sim" style={{ textDecoration: 'none', display: 'contents' }}> 
                <div className = "d-grid gap-2 col-1 mx-auto">
                    <Button variant ="success" size = "lg" title = "test button I">
                        Get Started 
                    </Button>
                </div>
            </Link>
            </div>
        </body>
    </>);
}



