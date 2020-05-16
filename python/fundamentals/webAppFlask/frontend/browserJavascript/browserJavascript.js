(async function main() {
  async function getCatData() {
    try {
      return (await axios.get('/cat')).data
    } catch(e) {
      return null;
    }
  }
  
  var cat = await getCatData();

  console.log(cat)
})()
