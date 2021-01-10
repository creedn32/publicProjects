import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {

  const [bankTransactionsArray, setBankTransactionsArray] = useState([]);
  // setBankTransactionsArray(['a', 'b', 'c']);
  // console.log(bankTransactionsArray);
  console.log('hi');



  return (
    <div className="App">
      <header className="App-header">
        Bank Transactions
      </header>
      <ul>
        {/* <BankTransactionsArray bankTransactionsArray={bankTransactionsArray}/> */}
      </ul>
    </div>
  );
}

export default App;
