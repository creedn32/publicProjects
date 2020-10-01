import React, { useState, useEffect } from 'react';
// import logo from './logo.svg';
import './App.css';
import Header from './Header';
import { setUserName } from '../action/actionCreators';
import { connect } from 'react-redux';

console.log("outside the function");


function App() {
  
  const [nameOfPerson, setNameOfPerson] = useState('Harry the Henderson');

  useEffect(() => {
    let newNameOfPerson = window.prompt('What is your name?', nameOfPerson);
    // setNameOfPerson(newNameOfPerson);
  }, []);

  return (
    <div className="App">
      <Header userName={nameOfPerson} setNameOfPerson={setNameOfPerson}/>
    </div>
  );
}

const mapStateToProps = (state, props) => {
  
}

export default connect(mapStateToProps)(App);
