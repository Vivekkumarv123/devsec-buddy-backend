// routes/scanRoutes.js

import express from "express";
import { runSecurityScan } from "../controllers/scanController.js";

const router = express.Router();

// POST /api/scan
router.post("/scan", runSecurityScan);

export default router;
