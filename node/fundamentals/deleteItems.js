const typesToDelete = ['User', 'Task'];

const activitiesTable = [
  [1, 'User', 2],
  [2, 'User', 1],
  [3, 'User', 4],
  [4, 'User', 3],
  [5, 'Task', 3],
  [6, 'Task', 4],
  [7, 'Task', 5],
];

const usersTable = [
  [1, '202001'],
  [2, null],
  [3, null],
  [4, null],
  [5, '202002'],
  [6, null]
];

const tasksTable = [
  [1, null],
  [2, null],
  [3, null],
  [4, null],
  [5, '202003'],
  [6, null]
];


typesToDelete.forEach((typeToDeleteElement) => {

  const filteredActivitiesTable = activitiesTable.filter(activity => {
    return activity[1] === typeToDeleteElement;
  });

  const recordsToDelete = {};
  const recordsNotToDelete = {};
  const tableName = typeToDeleteElement.toLowerCase() + 'sTable';

  filteredActivitiesTable.forEach((activitiesElement) => {

    if ((!(activitiesElement[2] in recordsToDelete)) && (!(activitiesElement[2] in recordsNotToDelete))) {
      tableElement = eval(tableName)[activitiesElement[2] - 1];
      if (tableElement[1] != null) {
        recordsToDelete[tableElement[0]] = tableElement[0];
      }
      else {
        recordsNotToDelete[tableElement[0]] = tableElement[0];
      }
    }
  });

  console.log('Delete these records from ' + tableName + ':');
  console.log(recordsToDelete);
  console.log('Dont delete these records from ' + tableName + ':');
  console.log(recordsToDelete);
  
});

