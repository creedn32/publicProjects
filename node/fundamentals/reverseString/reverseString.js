
function main() {

    //get input from commandline into array
    let inputArray = process.argv.splice(2);

    //get string from the input array
    let inputString = inputArray.join(' ');

    //split string into array
    let splitArray = inputString.split('');

    //reverse the array
    let reversedArray = splitArray.reverse();

    //join the reversed array
    let joinedString = reversedArray.join('');

    //print the reversed string
    console.log(joinedString);
}

main()