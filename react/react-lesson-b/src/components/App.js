import React, { useState, useEffect } from 'react';
// import logo from './logo.svg';
import './App.css';
import Header from './Header';
import { setUserName } from '../action/actionCreators';
import { connect } from 'react-redux';

console.log("outside the function");


function App(props) {
  
  useEffect(() => {
    let newNameOfPerson = window.prompt('What is your name?', props.nameOfPerson);
    props.setNameOfPerson(newNameOfPerson);
  }, []);

  return (
    <div className="App">
      <Header/>
    </div>
  );
}

const mapStateToProps = (state, props) => {
  return {
    nameOfPerson: state.username
  };
}

const mapDispatchToProps = (dispatch, props) => {
  return {
    setNameOfPerson: (nameOfPerson) => {
      const action = setUserName(nameOfPerson);
      dispatch(action);
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
