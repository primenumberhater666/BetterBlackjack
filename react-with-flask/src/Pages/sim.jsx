// import '../App.css'
import "../App.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form'; 
import Button from 'react-bootstrap/Button';

import NumberEntry from '../components/NumberEntry';
import List from '../components/List';
import SimSettings from "../components/SimSettings";

export function Sim() {


    return (
        <div class = "box"> 
            <List></List>
            <SimSettings></SimSettings>

        </div>
    );
    
}