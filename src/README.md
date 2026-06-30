# CampusEnergy — front end

Plain HTML/CSS/JS (no build step) for the CampusEnergy app: home, about, sign in, sign up,
profile, posts list, and post detail.

## Structure
```
campusenergy/
├── index.html       Home / landing
├── about.html        About Us
├── login.html        Sign in
├── signup.html       Sign up
├── profile.html       Logged-in user profile (renders differently for Student vs Faculty)
├── posts.html         List of posts
├── post.html           Single post + animated consumption chart (?id=p1)
└── shared/
    ├── styles.css     Design tokens + every component style + animations
    ├── api.js          All network calls live here
    └── app.js           Nav/footer mounting, toasts, reveal animations, form helpers
```

## Wiring up a real backend
Everything currently runs on in-memory mock data so the UI is fully clickable with no
server. To connect a real API:

1. In `shared/api.js`, set `window.__CE_USE_MOCKS__ = false` (e.g. in each page's `<head>`,
   before `api.js` loads) and set `window.__CE_API_BASE__ = "https://your-api.com/api/v1"`.
2. Update the `ENDPOINTS` map at the top of `api.js` if your routes differ from:
   - `POST /auth/login`, `POST /auth/signup`, `POST /auth/logout`
   - `GET /users/me`, `GET /users/:id`
   - `GET /posts`, `GET /posts/:id`
3. Every page already calls only `CampusEnergyAPI.*` methods — no other file needs to change.
4. Swap `persistSession`/`readSession` in `api.js` for cookie-based auth if your backend
   sets an httpOnly cookie instead of returning a token.

## Adding new pages
Drop a new `.html` file next to the others, then in its `<body>`:
```html
<div id="site-topbar"></div>
...your content...
<div id="site-footer"></div>
<script src="shared/api.js"></script>
<script src="shared/app.js"></script>
<script>CE.initAll({ topbar: { active: 'yourPageKey' } });</script>
```
`CE.initAll` mounts the nav + footer, wires button ripple/magnetic hover, and arms
scroll-reveal (`class="reveal"`) on any new elements.

## Notes
- Respects `prefers-reduced-motion`.
- All interactive elements are keyboard-focusable with a visible focus ring.
- Mock login accounts: `user@campusenergy.edu` (Student) and `prof@campusenergy.edu`
  (Faculty), any password.
