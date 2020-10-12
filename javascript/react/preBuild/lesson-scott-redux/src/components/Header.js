import React, { useState } from 'react';
import { connect } from 'react-redux';
// import logo from './logo.svg';
import Anchorlink from './Anchorlink';
import { setUserName } from '../action/actionCreators' 

function Header(props) {

  const [toggleState, setToggleState] = useState(true);
  
  const onNameChange = (event) => {
    let newNameOfPerson = event.target.value;
    props.setNameOfPerson(newNameOfPerson);
  }


  const [firstInput, setfirstInput] = useState('');
  const [secondInput, setsecondInput] = useState('');
  
  const onfirstInputChange = (event) => {
    setfirstInput(event.target.value);
  }  
  
  const onsecondInputChange = (event) => {
    setsecondInput(event.target.value);
  }


  const getOutput = () => {

    const firstNumber = Number.parseInt(firstInput);
    const secondNumber = Number.parseInt(secondInput);

    const isValid = !Number.isNaN(firstNumber) && !Number.isNaN(secondNumber);

    return isValid ? (firstNumber + secondNumber) : '';

  }


  function handleClick(event) {
    setToggleState(!toggleState);
  }


  return (
    <header className="App-header">
      Enter your name: <input type="text" onChange={onNameChange}/>
      <div onClick={handleClick}>
        {
          toggleState ? (<p>Hello, {props.username}!</p>) : (<p>Welcome, {props.username}, to this React site!</p>)
        } 
      </div>
      <Anchorlink nameOfUser={props.username}/>
      <p>Calculate the sum of two numbers:</p>
      <input type="text" onChange={onfirstInputChange} defaultValue={firstInput}/>&nbsp;+&nbsp;<input type="text" onChange={onsecondInputChange} defaultValue={secondInput}/> = {getOutput()}
    </header>
  );
}


const mapStateToProps = (state, props) => {
  return {
    username: state.username
  };
}

const mapDispatchToProps = (dispatch, props) => {
  return {
    ...props, 
    setNameOfPerson: (nameOfPerson) => {
      const action = setUserName(nameOfPerson);
      dispatch(action);
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Header);
