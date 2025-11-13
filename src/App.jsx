import { useState, useEffect } from 'react'
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from  "./Pages/home"
import { Sim } from './pages/sim';

import Button from 'react-bootstrap/Button';
import Title from "./components/Title"

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import './index.css'

function App() {

  return (
    <Router>
        <Routes>
            <Route path = "/" element = {<Home/>}/>
            <Route path = "/sim" element = {<Sim/>}/>
        </Routes>
    </Router>
  )
}


export default App
