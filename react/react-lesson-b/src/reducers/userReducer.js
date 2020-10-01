
export default const userReducer = (state, action) => {
    
    switch(action.type) {
        case 'SETUSERNAME':
            return {username: 'defaultUsername', };
        default:
            return state;
    }
}