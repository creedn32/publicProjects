
import { functionToCall } from './moduleToImport.mjs';

function mainFunction() {
    
    let a = 5;

    function printThis() {
        console.log(a);
        // console.log(b);
        let c = 7;
    }

    // console.log(c);
    functionToCall(printThis);
}

mainFunction();