import {
    AlertTriangle,
    Bot,
    CheckCircle2,
    FileText,
    User,
    XCircle,
} from "lucide-react";

import type {
    ChatMessage as ChatMessageType,
} from "../chat.types";


interface Props {
    message: ChatMessageType;
}


export function ChatMessage({
    message,
}: Props) {

    const isUser =
        message.role === "user";

    return (
        <div
            className={`
        flex gap-3
        ${isUser
                    ? "justify-end"
                    : "justify-start"
                }
      `}
        >
            {!isUser && (
                <div
                    className="
            flex h-9 w-9 shrink-0
            items-center justify-center
            rounded-full border bg-muted
          "
                >
                    <Bot className="h-5 w-5" />
                </div>
            )}

            <div
                className={`
          max-w-[80%]
          rounded-2xl
          px-4 py-3
          ${isUser
                        ? "bg-primary text-primary-foreground"
                        : "border bg-card"
                    }
        `}
            >
                {/* STATUS */}

                {!isUser && message.status && (
                    <div className="mb-2">
                        <StatusBadge
                            status={message.status}
                        />
                    </div>
                )}

                {/* MESSAGE */}

                <p
                    className="
            whitespace-pre-wrap
            text-sm leading-6
          "
                >
                    {message.content}
                </p>

                {/* SOURCES */}

                {!isUser &&
                    message.sources &&
                    message.sources.length > 0 && (
                        <div
                            className="
                mt-4 border-t pt-3
              "
                        >
                            <p
                                className="
                  mb-2 flex items-center
                  gap-1 text-xs font-medium
                  text-muted-foreground
                "
                            >
                                <FileText className="h-3.5 w-3.5" />

                                Sources
                            </p>

                            <div className="space-y-1">
                                {message.sources.map(
                                    (source) => (
                                        <div
                                            key={`${source.chunk_id}`}
                                            className="
                        rounded-md bg-muted
                        px-2 py-1.5
                        text-xs
                      "
                                        >
                                            {source.document_name}

                                            {source.page_number && (
                                                <span
                                                    className="
                            text-muted-foreground
                          "
                                                >
                                                    {" "}
                                                    · Page{" "}
                                                    {source.page_number}
                                                </span>
                                            )}
                                        </div>
                                    ),
                                )}
                            </div>
                        </div>
                    )}
            </div>

            {isUser && (
                <div
                    className="
            flex h-9 w-9 shrink-0
            items-center justify-center
            rounded-full bg-primary
            text-primary-foreground
          "
                >
                    <User className="h-5 w-5" />
                </div>
            )}
        </div>
    );
}


function StatusBadge({
    status,
}: {
    status: ChatMessageType["status"];
}) {

    if (
        status ===
        "answered_with_conflict"
    ) {
        return (
            <span
                className="
          inline-flex items-center gap-1
          rounded-full bg-yellow-100
          px-2 py-1 text-xs
          text-yellow-800
        "
            >
                <AlertTriangle className="h-3 w-3" />

                Conflicting information
            </span>
        );
    }

    if (status === "conflict") {
        return (
            <span
                className="
          inline-flex items-center gap-1
          rounded-full bg-orange-100
          px-2 py-1 text-xs
          text-orange-800
        "
            >
                <AlertTriangle className="h-3 w-3" />

                Source conflict
            </span>
        );
    }

    if (status === "not_found") {
        return (
            <span
                className="
          inline-flex items-center gap-1
          rounded-full bg-red-100
          px-2 py-1 text-xs
          text-red-700
        "
            >
                <XCircle className="h-3 w-3" />

                Not found
            </span>
        );
    }

    return (
        <span
            className="
        inline-flex items-center gap-1
        rounded-full bg-green-100
        px-2 py-1 text-xs
        text-green-700
      "
        >
            <CheckCircle2 className="h-3 w-3" />

            Grounded answer
        </span>
    );
}