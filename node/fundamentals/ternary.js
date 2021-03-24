const newArray = [1, 2, 3, 4];
const undefinedArray = undefined;

console.log(newArray.slice(1));
console.log(newArray.slice(undefinedArray?.length ? undefinedArray.length : 0));
console.log(newArray.slice(undefinedArray?.length ?? 0));

