// var path = require('path');
// var fs = require('fs');
// thisFilePathArray = path.resolve(__dirname, __filename).split(path.sep);
var c = console.log.bind(console);

const printArray = () => { 

    let arrExample = [
        {firstkey: 1, secondkey: 2},
        {firstkey: 3, secondkey: 4}
    ];

    arrExample2 = arrExample.filter((element) => {
        
        if (element.firstkey == 3) {
            return true;
        } 
        else {
            return false;
        }
    });
    
    arrExample2[0].firstkey = 5;
    c(arrExample);

};

module.exports = printArray;