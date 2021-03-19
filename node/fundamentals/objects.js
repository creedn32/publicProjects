const sampleFunc = () => {
  console.log('hi');
};

function otherSampleFunc() {
  console.log('buenos dias');
}

const sampleObj = {
  sampleValue: 1,
  sampleFunc
};

const secondSampleObj = {
  sampleFunc: sampleFunc
};

const thirdSampleObj = {
  secondSampleFunc: () => {
    console.log('hello');
  }
};

const fourthSampleObj = {
  secondSampleFunc: function() {
    console.log('good day');
  }
};

// const fifthSampleObj = {
//   function sayHi() {
//     console.log('Hi there');
//   }
// };

const sixthSampleObj = {
  otherSampleFunc
}


console.log(sampleObj);
sampleObj['sampleFunc']();
secondSampleObj['sampleFunc']();
thirdSampleObj['secondSampleFunc']();
fourthSampleObj['secondSampleFunc']();
// fifthSampleObj['sayHi']();
sixthSampleObj['otherSampleFunc']();