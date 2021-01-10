import PropTypes from 'prop-types';

const mapFn = (groceryItem, iterationCount) => (
    <li key={Math.round(Math.random() * 100)}>
      {groceryItem.toString()}
    </li>
);

const GroceryList = ({
  groceryList
}) => (
  <>
    {
      groceryList.map(mapFn)
    }
  </>
)

GroceryList.propTypes = {
  groceryList: PropTypes.arrayOf(PropTypes.string).isRequired,
}

export default GroceryList;