import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  const API_URL = 'http://localhost:8000';
  const FRONTEND_URL = 'http://localhost:3000';

  test.beforeEach(async ({ page }) => {
    // Wait for app to be ready
    await page.goto(FRONTEND_URL);
  });

  test('should display registration page', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/register`);
    
    await expect(page.locator('h1')).toContainText('Créer un compte');
    await expect(page.locator('input#email')).toBeVisible();
    await expect(page.locator('input#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should register a new user', async ({ page }) => {
    const timestamp = Date.now();
    const testUser = {
      email: `test${timestamp}@example.com`,
      password: 'testpassword123',
      name: 'Test User'
    };

    await page.goto(`${FRONTEND_URL}/register`);
    
    await page.fill('input#name', testUser.name);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    
    // Wait for redirect to home after successful registration
    await page.waitForURL(FRONTEND_URL + '/', { timeout: 5000 });
    
    // Verify user is logged in (should see user name or logout button)
    await expect(page.locator('.user-menu')).toBeVisible();
  });

  test('should not register with existing email', async ({ page }) => {
    // First register a user
    const timestamp = Date.now();
    const testUser = {
      email: `duplicate${timestamp}@example.com`,
      password: 'testpassword123'
    };

    await page.goto(`${FRONTEND_URL}/register`);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(FRONTEND_URL + '/', { timeout: 5000 });
    
    // Logout
    await page.click('button:has-text("Déconnexion")');
    
    // Try to register with same email
    await page.goto(`${FRONTEND_URL}/register`);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    
    // Should show error
    await expect(page.locator('.error-message')).toContainText('déjà utilisé');
  });

  test('should display login page', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/login`);
    
    await expect(page.locator('h1')).toContainText('Connexion');
    await expect(page.locator('input#email')).toBeVisible();
    await expect(page.locator('input#password')).toBeVisible();
  });

  test('should login with valid credentials', async ({ page }) => {
    // First create a user
    const timestamp = Date.now();
    const testUser = {
      email: `logintest${timestamp}@example.com`,
      password: 'mypassword123'
    };

    await page.goto(`${FRONTEND_URL}/register`);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(FRONTEND_URL + '/', { timeout: 5000 });
    
    // Logout
    await page.click('button:has-text("Déconnexion")');
    
    // Login
    await page.goto(`${FRONTEND_URL}/login`);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    
    // Should redirect to home and show user menu
    await page.waitForURL(FRONTEND_URL + '/', { timeout: 5000 });
    await expect(page.locator('.user-menu')).toBeVisible();
  });

  test('should not login with invalid credentials', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/login`);
    
    await page.fill('input#email', 'nonexistent@example.com');
    await page.fill('input#password', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Should show error
    await expect(page.locator('.error-message')).toContainText('incorrect');
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    const timestamp = Date.now();
    const testUser = {
      email: `logouttest${timestamp}@example.com`,
      password: 'testpass123'
    };

    await page.goto(`${FRONTEND_URL}/register`);
    await page.fill('input#email', testUser.email);
    await page.fill('input#password', testUser.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(FRONTEND_URL + '/', { timeout: 5000 });
    
    // Verify logged in
    await expect(page.locator('.user-menu')).toBeVisible();
    
    // Logout
    await page.click('button:has-text("Déconnexion")');
    
    // Should show login/register buttons
    await expect(page.locator('.auth-buttons')).toBeVisible();
  });
});
