export const aiConfig = {
    baseUrl:
        process.env.AI_SERVICE_URL ??
        "http://127.0.0.1:8000",

    timeoutMs: Number(
        process.env.AI_SERVICE_TIMEOUT_MS ?? 120000
    ),
    apiKey:
        process.env.AI_SERVICE_API_KEY ?? "",
};