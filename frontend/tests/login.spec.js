import { test, expect } from '@playwright/test';

test('User should be able to log in successfully', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Log in' }).click();
  await page.locator('input[type="email"]').fill('itsmeunicorn@mail.com');
  await page.locator('input[type="password"]').fill('12345');
  await page.getByRole('button', { name: 'Log in' }).click();
  await expect(page).toHaveURL(/.*dashboard/);
});
