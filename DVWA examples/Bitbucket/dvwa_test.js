const { chromium } = require('playwright');

(async () => {
  const useProxy = process.env.RUNNING_FROM_PYNT;

  const launchOptions = {
    headless: false,
    args: ['--ignore-certificate-errors']
  };

  const contextOptions = {
    ignoreHTTPSErrors: true
  };

  if (useProxy) {
    contextOptions.proxy = {
      server: 'http://127.0.0.1:6666',
      bypass: '<-loopback>'
    };
    console.log('Using proxy with certificate ignoring and bypass:');
    console.log(contextOptions);
  } else {
    console.log('Not using a proxy');
  }

  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext(contextOptions);
  const page = await context.newPage();


  const host = 'localhost:80'; 

  // First login
  await page.goto(`http://${host}/login.php`);
  await page.locator('input[name="username"]').fill('admin');
  await page.locator('input[name="password"]').fill('password');
  await page.locator('input[name="password"]').press('Enter');

  // Try to reset DB
  const resetButton = await page.$('input[value="Create / Reset Database"]');
  if (resetButton) {
    await resetButton.click();
    console.log('Clicked "Create / Reset Database" button');
  } else {
    console.log('"Create / Reset Database" button not found — continuing...');
  }

  // Second login (post-reset)
  await page.goto(`http://${host}/login.php`);
  await page.locator('input[name="username"]').fill('admin');
  await page.locator('input[name="password"]').fill('password');
  await page.locator('input[name="password"]').press('Enter');

  // SQL Injection page
  await page.waitForSelector('a[href="vulnerabilities/sqli/"]');
  await page.click('a[href="vulnerabilities/sqli/"]');
  console.log('Navigated to SQL Injection page');

  await page.getByRole('textbox').click();
  await page.getByRole('textbox').fill('1');
  await page.getByRole('button', { name: 'Submit' }).click();

  await context.close();
  await browser.close();
})();
