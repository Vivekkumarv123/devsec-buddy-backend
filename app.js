// app.js or server.js

import express from "express";
import cors from "cors";
import helmet from "helmet"; // ✅ Security headers
import scanRoutes from "./routes/scanRoutes.js";

const app = express();

// Middlewares
app.use(cors());
app.use(helmet()); // ✅ Automatically sets many secure headers
app.use(express.json());

// Optional: Custom headers for extra protection
app.use((req, res, next) => {
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=()");
  next();
});

// Routes
app.use("/api", scanRoutes);

// Root
app.get("/", (req, res) => {
  res.send("🚀 DevSec Buddy backend is running!");
});

// Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
