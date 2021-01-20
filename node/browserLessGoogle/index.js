
const puppeteer = require('puppeteer');

(async() => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  module.exports = async ({ page }) => {
  await page.goto('https://www.google.com');
};
      
  browser.close();
})();
