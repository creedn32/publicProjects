function foo(staticParts, dynamicParts) {
  console.log('staticParts', staticParts);
  console.log('dynamicParts', dynamicParts);
}

foo`this is a ${42} test`