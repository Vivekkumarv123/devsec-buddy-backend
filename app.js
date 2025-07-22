import express from "express";
import cors from "cors";
import helmet from "helmet";
import scanRoutes from "./routes/scanRoutes.js";

const app = express();

const allowedOrigins = [
  "http://localhost:3000",
  "https://devsec-buddy-frontend.vercel.app",
];

// Apply CORS (update as needed)
app.use(cors({
  origin: allowedOrigins
}));

// Use Helmet with advanced config for full security header coverage
app.use(helmet({
  contentSecurityPolicy: {
    useDefaults: true,
    directives: {
      "default-src": ["'self'"],
      "script-src": ["'self'"],
      "style-src": ["'self'", "'unsafe-inline'"], // Allow Tailwind CSS etc.
      "img-src": ["'self'", "data:"],
      "font-src": ["'self'", "https:", "data:"],
      "connect-src": ["'self'", "*"], // For API requests (limit if needed)
    }
  },
  referrerPolicy: { policy: "no-referrer" },
  crossOriginEmbedderPolicy: false // Avoid issues with 3rd-party embeds
}));

// Parse JSON requests
app.use(express.json());

// Manually set headers not fully covered by helmet
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  res.setHeader("X-XSS-Protection", "1; mode=block");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
  next();
});

// Health check
app.get("/healthz", (req, res) => res.send("OK, Working Well!"));

// API routes
app.use("/api", scanRoutes);

// Default root route
app.get("/", (req, res) => {
  res.send("🚀 DevSec Buddy backend is running!");
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
