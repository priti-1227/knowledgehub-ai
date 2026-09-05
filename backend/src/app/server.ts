import app from "./app.js";
import { env } from "../config/env.js";
import "../workers/ai-indexing.worker.js";
app.listen(env.port, () => {
    console.log(`🚀 Server running on http://localhost:${env.port}`);
});
