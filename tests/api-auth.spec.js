import { test, expect, request } from '@playwright/test';

const API_URL = 'http://localhost:8000';

test.describe('Backend API - Authentication', () => {
  let authToken = null;
  const timestamp = Date.now();
  const testUser = {
    email: `apitest${timestamp}@example.com`,
    password: 'testpassword123',
    name: 'API Test User'
  };

  test('should register a new user via API', async () => {
    const api = await request.newContext();
    
    const response = await api.post(`${API_URL}/api/register`, {
      data: testUser
    });
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.token).toBeDefined();
    expect(data.user.email).toBe(testUser.email);
    
    authToken = data.token;
  });

  test('should not register with duplicate email', async () => {
    const api = await request.newContext();
    
    // Try to register same user again
    const response = await api.post(`${API_URL}/api/register`, {
      data: testUser
    });
    
    expect(response.status()).toBe(400);
    
    const data = await response.json();
    expect(data.detail).toContain('déjà utilisé');
  });

  test('should login with valid credentials', async () => {
    const api = await request.newContext();
    
    const response = await api.post(`${API_URL}/api/login`, {
      data: {
        email: testUser.email,
        password: testUser.password
      }
    });
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.token).toBeDefined();
    expect(data.user.email).toBe(testUser.email);
  });

  test('should not login with invalid credentials', async () => {
    const api = await request.newContext();
    
    const response = await api.post(`${API_URL}/api/login`, {
      data: {
        email: testUser.email,
        password: 'wrongpassword'
      }
    });
    
    expect(response.status()).toBe(401);
    
    const data = await response.json();
    expect(data.detail).toContain('incorrect');
  });

  test('should get user profile with valid token', async () => {
    const api = await request.newContext();
    
    // First login to get token
    const loginResponse = await api.post(`${API_URL}/api/login`, {
      data: {
        email: testUser.email,
        password: testUser.password
      }
    });
    
    const { token } = await loginResponse.json();
    
    // Get user profile
    const response = await api.get(`${API_URL}/api/me`, {
      headers: { 'Authorization': token }
    });
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.email).toBe(testUser.email);
    expect(data.name).toBe(testUser.name);
  });

  test('should not get user profile without token', async () => {
    const api = await request.newContext();
    
    const response = await api.get(`${API_URL}/api/me`);
    
    expect(response.status()).toBe(401);
  });

  test('should logout successfully', async () => {
    const api = await request.newContext();
    
    // First login
    const loginResponse = await api.post(`${API_URL}/api/login`, {
      data: {
        email: testUser.email,
        password: testUser.password
      }
    });
    
    const { token } = await loginResponse.json();
    
    // Logout
    const response = await api.post(`${API_URL}/api/logout`, {
      headers: { 'Authorization': token }
    });
    
    expect(response.ok()).toBeTruthy();
    
    // Token should be invalidated
    const meResponse = await api.get(`${API_URL}/api/me`, {
      headers: { 'Authorization': token }
    });
    
    expect(meResponse.status()).toBe(401);
  });
});
