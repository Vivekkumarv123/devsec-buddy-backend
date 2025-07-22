import express from "express";
import cors from "cors";
import helmet from "helmet";
import scanRoutes from "./routes/scanRoutes.js";

const app = express();

// Replace this with your actual frontend URL
const allowedOrigin = "http://localhost:3000";

// Middlewares
app.use(cors({
  origin: allowedOrigin
}));
app.use(helmet()); // Security headers
app.use(express.json());

// Extra custom security headers
app.use((req, res, next) => {
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=()");
  next();
});

// Health check route
app.get('/healthz', (req, res) => res.send('OK, Working Well!'));

// API routes
app.use("/api", scanRoutes);

// Root route
app.get("/", (req, res) => {
  res.send("🚀 DevSec Buddy backend is running!");
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
