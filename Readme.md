# 🛡️ DevSec Buddy – Backend

A modular, extensible Node.js backend for **DevSec Buddy**, an open-source local web security scanner. Supports deep security scan profiles and integration with a Python-based vulnerability scanner.

---

## 🚀 Features

- REST API to trigger security scans via `/api/scan`
- Supports modular scan profiles: `basic`, `standard`, `deep`
- Handles custom request:
  - `method` (`GET`, `POST`, etc.)
  - `headers`
  - `cookies`
  - `body data`
- Dynamically invokes Python scanner (`scanner/main.py`)
- Auto-prewake for Render-based backend URLs to prevent cold start lag
- Clean error handling and JSON output

---

## 📁 Folder Structure
````
backend/
├── controllers/
│ └── scanController.js
├── routes/
│ └── scanRoutes.js # Router for /api/scan
├── scanner/
│ └── main.py # Python scanner entry
└── index.js # Express server entry point

````


## 📦 Requirements

- Node.js 18+ or 20+ (ESM support required)
- Python 3.8+
- Express.js
- Nodemon (for dev)
- Axios (used for Render pre-wake)

---

## 📡 API Endpoint

### `POST /api/scan`

Runs a security scan using the specified profile.

#### 🔸 Request Body

```json
{
  "url": "https://target-site.com",
  "profile": "basic",
  "method": "POST",
  "data": { "username": "admin" },
  "headers": { "Authorization": "Bearer token" },
  "cookies": { "session": "abc123" }
}
url (string): URL to scan (required)

profile (string): One of basic, standard, or deep (optional, default = basic)

method, data, headers, cookies are optional and support advanced scans

🔹 Sample Response
json
Copy
Edit
{
  "success": true,
  "results": {
    "vulnerabilities": [...],
    "summary": { "score": 72, "severity": "medium" }
  }
}
```
⚙️ Render Cold Start Handling
If the scan target is https://devsec-buddy-backend.onrender.com, the backend will automatically ping /healthz to pre-wake Render.

```
if (input.url.includes("devsec-buddy-backend.onrender.com")) {
  await axios.get("https://devsec-buddy-backend.onrender.com/healthz");
}
```

This reduces cold start time during internal scans.

🧪 Dev Setup
```
# Clone
git clone https://github.com/your-username/devsec-buddy.git
cd devsec-buddy/backend

# Install dependencies
npm install

# Start server
npm run dev
Make sure your Python scanner is ready at scanner/main.py

🤝 Contributing
Fork the repo

Create your feature branch (git checkout -b feature/something)

Commit your changes (git commit -am 'Add something')

Push to the branch (git push origin feature/something)

Open a Pull Request
```

# License
MIT License © 2025 



## ✨ Credits

Created by **Vivek Kumar Verma** 👨‍💻
Connect on [LinkedIn](https://www.linkedin.com/in/vivek-kumar-verma-programmer-information-technology/) or visit [GitHub](https://github.com/Vivekkumarv123)

