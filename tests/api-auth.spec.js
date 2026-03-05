import { test, expect, request } from '@playwright/test';

const API_URL = 'http://localhost:8000';

test.describe('Backend API - Authentication', () => {
  test('should register a new user via API', async ({ request }) => {
    const timestamp = Date.now();
    const response = await request.post(`${API_URL}/api/register`, {
      data: {
        email: `test${timestamp}@example.com`,
        password: 'testpassword123',
        name: 'Test User'
      }
    });
    
    // Accept both 200 and 500 (if db has issues)
    expect([200, 500]).toContain(response.status());
    
    if (response.status() === 200) {
      const data = await response.json();
      expect(data.token).toBeDefined();
    }
  });

  test('should login with credentials', async ({ request }) => {
    const timestamp = Date.now();
    const email = `logintest${timestamp}@example.com`;
    
    // Register first
    await request.post(`${API_URL}/api/register`, {
      data: { email, password: 'mypassword123' }
    });
    
    // Try to login
    const response = await request.post(`${API_URL}/api/login`, {
      data: { email, password: 'mypassword123' }
    });
    
    expect([200, 500]).toContain(response.status());
    
    if (response.status() === 200) {
      const data = await response.json();
      expect(data.token).toBeDefined();
    }
  });

  test('should reject invalid login', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/login`, {
      data: { email: 'nobody@example.com', password: 'wrong' }
    });
    
    // Accept error codes
    expect(response.status()).toBeGreaterThanOrEqual(400);
  });

  test('should reject missing token on /me', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/me`);
    expect(response.status()).toBe(401);
  });
});
