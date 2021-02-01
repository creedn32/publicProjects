const c = console.log.bind(console);
const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(stealthPlugin);

const browserlessGoogle = async ([...loginCredentials]) => {

  let [ username, password ] = loginCredentials;

  if (!loginCredentials.length) {

    ({ username, password } = require('../../../privateData/node/puppeteerGoogle/loginData'));

  }
  
  // c(username);
  // c(password);

  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  const navigationPromise = page.waitForNavigation();

  await page.goto('https://www.google.com');

  signInSelector = '.gb_be.gb_4.gb_5c';
  await page.waitForSelector(signInSelector);
  await page.click(signInSelector);

  emailInputSelector = 'input[type="email"]';
  await page.waitForSelector(emailInputSelector);
  await page.type(emailInputSelector, username);

  await page.click("#identifierNext");
  await navigationPromise;

  // await page.waitForSelector(, { visible: true });
  // await page.type(, username);

  // await page.waitForSelector("#passwordNext", { visible: true });
  // await page.click("#passwordNext");

  // await browser.close();
  // await page.screenshot({path: 'screenshot.png'});

};

module.exports = browserlessGoogle;
