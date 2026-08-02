import type { DocumentsResponse } from "../types/document";

const API = `${import.meta.env.VITE_API_URL}/api/documents`;

const headers = () => ({
    Authorization:
        `Bearer ${localStorage.getItem("token")}`,
});

export const documentApi = {

    async getAll(): Promise<DocumentsResponse> {

        const res = await fetch(API, {
            headers: headers(),
        });

        if (!res.ok)
            throw new Error("Failed to fetch documents");

        return res.json();
    },

    async upload(formData: FormData) {

        const res = await fetch(
            `${API}/upload`,
            {
                method: "POST",

                headers: {
                    Authorization:
                        `Bearer ${localStorage.getItem("token")}`,
                },

                body: formData,
            }
        );

        if (!res.ok)
            throw new Error("Upload failed");

        return res.json();
    },

    async delete(id: string) {

        const res = await fetch(
            `${API}/${id}`,
            {
                method: "DELETE",

                headers: headers(),
            }
        );

        if (!res.ok)
            throw new Error("Delete failed");

        return res.json();
    },
    async download(id: string, defaultFileName?: string) {
        const response = await fetch(
            `${API}/${id}/download`,
            {
                headers: headers(),
            }
        );

        if (!response.ok)
            throw new Error("Download failed");

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        let filename = defaultFileName || "document";
        const disposition = response.headers.get("content-disposition");
        if (disposition && disposition.includes("filename=")) {
            const matches = /filename="?([^";]+)"?/.exec(disposition);
            if (matches?.[1]) {
                filename = matches[1];
            }
        }

        const a = document.createElement("a");
        a.href = url;
        a.setAttribute("download", filename);
        document.body.appendChild(a);
        a.click();
        a.remove();

        URL.revokeObjectURL(url);
    },
    async view(id: string) {
        const response = await fetch(
            `${API}/${id}/view`,
            {
                headers: headers(),
            }
        );

        const url = URL.createObjectURL(await response.blob());

        window.open(url, "_blank");
    }

};