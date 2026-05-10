import { test, expect } from '@playwright/test';

test('Hayalet kullanıcı siteye girer ve fotoğraf çeker', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'kanit.png' });
});