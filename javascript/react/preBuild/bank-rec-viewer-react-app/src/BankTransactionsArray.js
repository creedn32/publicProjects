import PropTypes from 'prop-types';

const mapFn = (bankTransaction, bankTransactionIndex) => (
    <li key={Math.round(Math.random() * 100)}>
      {bankTransaction.toString()}
    </li>
);

const BankTransactionsArray = ({bankTransactionsArray}) => (
  <>
    {
      bankTransactionsArray.map(mapFn)
    }
  </>
)

BankTransactionsArray.propTypes = {
  bankTransactionsArray: PropTypes.arrayOf(PropTypes.string).isRequired,
}

export default BankTransactionsArray;