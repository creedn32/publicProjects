const defaultState = {username: 'Harry the Henderson'};

export default (state=defaultState, action) => {

    switch(action.type) {
        case 'SETUSERNAME':
            return {username: action.username, };
        default:
            return state;
    }
}