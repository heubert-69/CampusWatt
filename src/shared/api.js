/* =========================================================
   CampusEnergy — API layer
   Centralizes every network call so the rest of the app never
   talks to fetch() directly. Swap BASE_URL / endpoints here
   when the real backend is ready — nothing else needs to change.

   Until USE_MOCKS is set to false, every call resolves against
   an in-memory mock so the UI is fully clickable without a server.
   ========================================================= */

const CampusEnergyAPI = (() => {

  const CONFIG = {
    BASE_URL: window.__CE_API_BASE__ || '/api/v1',
    USE_MOCKS: window.__CE_USE_MOCKS__ !== false, // default true until a backend exists
    TIMEOUT_MS: 12000,
  };

  const ENDPOINTS = {
    login:        () => `${CONFIG.BASE_URL}/auth/login`,
    signup:       () => `${CONFIG.BASE_URL}/auth/signup`,
    logout:       () => `${CONFIG.BASE_URL}/auth/logout`,
    me:           () => `${CONFIG.BASE_URL}/users/me`,
    profile:      (id) => `${CONFIG.BASE_URL}/users/${id}`,
    posts:        () => `${CONFIG.BASE_URL}/posts`,
    post:         (id) => `${CONFIG.BASE_URL}/posts/${id}`,
    consumption:  (postId) => `${CONFIG.BASE_URL}/posts/${postId}/consumption`,
  };

  async function request(url, options = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), CONFIG.TIMEOUT_MS);
    try {
      const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
        credentials: 'include',
        signal: controller.signal,
        ...options,
      });
      clearTimeout(timer);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new APIError(body.message || `Request failed (${res.status})`, res.status, body);
      }
      return res.status === 204 ? null : res.json();
    } catch (err) {
      clearTimeout(timer);
      throw err instanceof APIError ? err : new APIError(err.message || 'Network error', 0);
    }
  }

  class APIError extends Error {
    constructor(message, status, body) {
      super(message);
      this.name = 'APIError';
      this.status = status;
      this.body = body;
    }
  }

  /* ---------------- Mock data + latency simulation ---------------- */

  const delay = (ms = 500) => new Promise((r) => setTimeout(r, ms));

  const MOCK_USERS = {
    'user@campusenergy.edu':  { id: 'u1', username: 'User',  email: 'user@campusenergy.edu',  age: 21, userType: 'Student', course: 'BS IT', about: 'This is a text about me.' },
    'prof@campusenergy.edu':  { id: 'u2', username: 'User2', email: 'prof@campusenergy.edu',   age: 21, userType: 'Faculty', position: 'Professor', about: 'This is a text about me.' },
  };

  const MOCK_POSTS = [
    { id: 'p1', title: 'Post About Energy Conservation', author: 'User2', authorId: 'u2', date: '06/25/26', insight: 'Evening peak draw is trending down 4% week over week after the dorm lighting retrofit.', data: [39, 3, 94, 69, 76, 5, 36, 25, 52, 16, 75, 28] },
    { id: 'p2', title: 'Library Wing — Weekend Idle Load', author: 'User', authorId: 'u1', date: '06/24/26', insight: 'Idle HVAC overnight accounts for nearly a third of weekend usage.', data: [12, 18, 22, 14, 9, 31, 28, 19, 24, 17, 11, 8] },
    { id: 'p3', title: 'Solar Array — June Output Recap', author: 'User2', authorId: 'u2', date: '06/20/26', insight: 'Panel output peaked mid-month during the clear-sky stretch.', data: [55, 61, 70, 82, 90, 88, 76, 64, 58, 49, 41, 37] },
    { id: 'p4', title: 'Cafeteria Refrigeration Audit', author: 'User', authorId: 'u1', date: '06/18/26', insight: 'Two compressors are cycling far more often than spec — flagged for maintenance.', data: [44, 47, 52, 58, 61, 59, 55, 50, 46, 48, 53, 57] },
    { id: 'p5', title: 'Dorm Block C — Move-in Week Spike', author: 'User2', authorId: 'u2', date: '06/12/26', insight: 'Expected seasonal spike from appliance setup; normalized by day five.', data: [20, 35, 60, 82, 71, 58, 44, 33, 29, 26, 24, 22] },
  ];

  let mockSession = null; // { token, user }

  function getEndpoints() {
    return ENDPOINTS;
  }

  /* ---------------- Public methods ---------------- */

  async function login({ email, password }) {
    if (CONFIG.USE_MOCKS) {
      await delay(700);
      const user = MOCK_USERS[email.trim().toLowerCase()];
      if (!user || !password) throw new APIError('Email or password is incorrect.', 401);
      mockSession = { token: 'mock-token', user };
      persistSession(mockSession);
      return mockSession;
    }
    const data = await request(ENDPOINTS.login(), { method: 'POST', body: JSON.stringify({ email, password }) });
    persistSession(data);
    return data;
  }

  async function signup({ username, email, password, confirmPassword }) {
    if (CONFIG.USE_MOCKS) {
      await delay(800);
      if (password !== confirmPassword) throw new APIError('Passwords do not match.', 400);
      const user = { id: 'u_' + Date.now(), username, email, age: null, userType: 'Student', course: '', about: '' };
      MOCK_USERS[email.trim().toLowerCase()] = user;
      mockSession = { token: 'mock-token', user };
      persistSession(mockSession);
      return mockSession;
    }
    const data = await request(ENDPOINTS.signup(), { method: 'POST', body: JSON.stringify({ username, email, password, confirmPassword }) });
    persistSession(data);
    return data;
  }

  async function logout() {
    clearSession();
    if (CONFIG.USE_MOCKS) { await delay(200); return true; }
    return request(ENDPOINTS.logout(), { method: 'POST' });
  }

  async function getCurrentUser() {
    const session = readSession();
    if (CONFIG.USE_MOCKS) {
      await delay(300);
      return session ? session.user : null;
    }
    if (!session) return null;
    return request(ENDPOINTS.me());
  }

  async function getPosts() {
    if (CONFIG.USE_MOCKS) { await delay(500); return MOCK_POSTS; }
    return request(ENDPOINTS.posts());
  }

  async function getPost(id) {
    if (CONFIG.USE_MOCKS) {
      await delay(450);
      const post = MOCK_POSTS.find((p) => p.id === id) || MOCK_POSTS[0];
      return post;
    }
    return request(ENDPOINTS.post(id));
  }

  /* ---------------- Session persistence (swap for real auth/cookies) ---------------- */

  function persistSession(session) {
    try { sessionStorage.setItem('ce_session', JSON.stringify(session)); } catch (e) {}
  }
  function readSession() {
    try { return JSON.parse(sessionStorage.getItem('ce_session')); } catch (e) { return null; }
  }
  function clearSession() {
    try { sessionStorage.removeItem('ce_session'); } catch (e) {}
  }

  return {
    config: CONFIG,
    endpoints: getEndpoints(),
    login,
    signup,
    logout,
    getCurrentUser,
    getPosts,
    getPost,
    readSession,
    APIError,
  };
})();
