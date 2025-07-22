// controllers/scanController.js

import { spawn } from "child_process";
import axios from "axios";

/**
 * POST /api/scan
 */
export const runSecurityScan = async (req, res) => {
  try {
    const input = {
      url: req.body.url,
      profile: req.body.profile || "basic",
      method: req.body.method || "POST",
      data: req.body.data || null,
      headers: req.body.headers || null,
      cookies: req.body.cookies || null,
    };

    // ✅ Pre-wake Render backend if scanned URL is your own server
    if (input.url.includes("devsec-buddy-backend.onrender.com")) {
      try {
        await axios.get("https://devsec-buddy-backend.onrender.com/healthz", {
          timeout: 10000,
        });
        console.log("✅ Pre-wake successful for Render");
      } catch (err) {
        console.warn("⚠️ Pre-wake failed:", err.message);
      }
    }

    const python = spawn("python", ["scanner/main.py"]);

    let output = "";
    let errorOutput = "";

    python.stdin.write(JSON.stringify(input));
    python.stdin.end();

    python.stdout.on("data", (data) => {
      output += data.toString();
    });

    python.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    python.on("close", (code) => {
      if (code !== 0 || errorOutput) {
        return res.status(500).json({
          success: false,
          message: "Scanner execution failed",
          error: errorOutput || "Unknown error",
        });
      }

      try {
        const results = JSON.parse(output);
        return res.json({
          success: true,
          results,
        });
      } catch (err) {
        return res.status(500).json({
          success: false,
          message: "Invalid JSON from scanner",
          raw: output,
        });
      }
    });
  } catch (err) {
    return res.status(500).json({
      success: false,
      message: "Scan controller error",
      error: err.message,
    });
  }
};
