// app.js or server.js

import express from "express";
import cors from "cors";
import scanRoutes from "./routes/scanRoutes.js";

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

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
