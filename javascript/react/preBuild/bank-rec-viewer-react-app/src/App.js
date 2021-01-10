import logo from './logo.svg';
import './App.css';

function App() {

  // const [groceryList, setGroceryList] = useState([]);
  // const [input, setInput] = useState('');

  // const onInputChange = e => {
  //   setInput(e.target.value);
  // }

  // const onButtonClick = () => {
  //   const newGroceryItem = input;

  //   addToGroceryList();    
  // }
  
  // const onInputKeyPress = e => {
  //     if(e.key === 'Enter'){
  //       addToGroceryList();
  //     }
  // }
  
  // const addToGroceryList = () => {
  //   setGroceryList([...groceryList, input]);
  //   setInput('');
  // }


  return (
    <div className="App">
      <header className="App-header">
        Bank Transactions
      </header>
      <ul>
        {/* <GroceryList groceryList={groceryList}/> */}
      </ul>
    </div>
  );
}

export default App;
