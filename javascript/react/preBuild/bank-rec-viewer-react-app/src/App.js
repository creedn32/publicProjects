import './App.css';
import { useState } from 'react';
import { initialBankTransactionsArray } from './data/sampleData'

function App() {

  const [bankTransactionsArray, setBankTransactionsArray] = useState(initialBankTransactionsArray);

  return (
    <div className="App">
      <header className="App-header">
        Bank Transactions
      </header>
      <ul>
        {bankTransactionsArray.map(bankTransaction => (
          <li>{bankTransaction}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
