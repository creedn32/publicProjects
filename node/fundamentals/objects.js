const sampleFunc = () => {
  console.log('hi');
}

const mealsForADay = [{
  calories: 500,
  name: 'Scott'
}, {
  calories: 3000,
  name: 'Scott'
}, {
  calories: 1,
  name: 'Creed'
}, {
  calories: 2,
  name: 'Creed'
}]

const personToCalories = mealsForADay
  .reduce((accum, meal) => {

    const { name, calories: caloriesInAMeal } = meal;
    const previouslyStoredCalories = accum[name] ?? 0;

    const totalCalories = previouslyStoredCalories + caloriesInAMeal;

    return {
      ...accum,
      [name]: totalCalories,
    }
  }, {})

  console.log(personToCalories);