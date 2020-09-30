import React from 'react';
import { connect } from 'react-redux';

function AnchorlinkMarkup(props) {
    return (
        <a
        className="App-link"
        href="https://reactjs.org"
        target="_blank"
        rel="noopener noreferrer">
        Learn a little bit of React, {props.username}
        </a>
    )
}

export default connect (mapStateToProps) (AnchorlinkMarkup);

function mapStateToProps(state, props) {
    return {
        username: state.user.username
    };
}
