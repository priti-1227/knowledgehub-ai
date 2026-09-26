import type {
    ChatApiResponse,
} from "./chat.types";


const API_BASE_URL =
    import.meta.env.VITE_API_URL ??
    "http://localhost:5000";


interface ApiResponse<T> {
    success: boolean;
    data: T;
    message?: string;
}


export async function askAI(
    question: string,
): Promise<ChatApiResponse> {

    const token =
        localStorage.getItem("accessToken") ??
        localStorage.getItem("token");

    const response = await fetch(
        `${API_BASE_URL}/api/v1/chat`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",

                ...(token
                    ? {
                        Authorization:
                            `Bearer ${token}`,
                    }
                    : {}),
            },

            body: JSON.stringify({
                question,
            }),
        },
    );

    if (!response.ok) {

        let message =
            "Failed to get response from AI.";

        try {
            const errorData =
                await response.json();

            message =
                errorData.message ??
                errorData.detail ??
                errorData.error ??
                message;

        } catch {
            // Keep default message.
        }

        throw new Error(message);
    }

    const result:
        ApiResponse<ChatApiResponse> =
        await response.json();

    // Node wraps FastAPI response inside:
    //
    // {
    //   success: true,
    //   data: {...}
    // }
    //
    // We return only data to ChatPage.

    return result.data;
}