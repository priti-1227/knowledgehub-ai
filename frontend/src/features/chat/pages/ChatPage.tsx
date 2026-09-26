import {
    type FormEvent,
    useState,
} from "react";

import {
    Loader2,
    Send,
    Sparkles,
} from "lucide-react";

import {
    askAI,
} from "../chat.api";

import type {
    ChatMessage,
} from "../chat.types";

import {
    ChatMessage as ChatMessageComponent,
} from "../components/ChatMessage";


export default function ChatPage() {

    const [
        question,
        setQuestion,
    ] = useState("");

    const [
        messages,
        setMessages,
    ] = useState<ChatMessage[]>([]);

    const [
        loading,
        setLoading,
    ] = useState(false);

    const [
        error,
        setError,
    ] = useState<string | null>(
        null,
    );


    async function handleSubmit(
        event: FormEvent,
    ) {

        event.preventDefault();

        const trimmedQuestion =
            question.trim();

        if (
            !trimmedQuestion ||
            loading
        ) {
            return;
        }

        setError(null);

        const userMessage: ChatMessage = {
            id: crypto.randomUUID(),

            role: "user",

            content: trimmedQuestion,
        };

        setMessages(
            (previous) => [
                ...previous,
                userMessage,
            ],
        );

        setQuestion("");
        setLoading(true);

        try {

            const response =
                await askAI(
                    trimmedQuestion,
                );

            const assistantMessage:
                ChatMessage = {

                id: crypto.randomUUID(),

                role: "assistant",

                content:
                    response.answer,

                status:
                    response.answer_status,

                grounded:
                    response.grounded,

                conflict:
                    response.conflict,

                sources:
                    response.sources ?? [],
            };

            setMessages(
                (previous) => [
                    ...previous,
                    assistantMessage,
                ],
            );

        } catch (error) {

            const message =
                error instanceof Error
                    ? error.message
                    : "Something went wrong.";

            setError(message);

        } finally {

            setLoading(false);
        }
    }


    return (
        <div
            className="
        flex min-h-screen
        flex-col bg-background
      "
        >
            {/* HEADER */}

            <header
                className="
          border-b bg-card
        "
            >
                <div
                    className="
            mx-auto flex
            max-w-5xl
            items-center gap-3
            px-6 py-4
          "
                >
                    <div
                        className="
              flex h-10 w-10
              items-center justify-center
              rounded-xl bg-primary
              text-primary-foreground
            "
                    >
                        <Sparkles className="h-5 w-5" />
                    </div>

                    <div>
                        <h1
                            className="
                text-lg font-semibold
              "
                        >
                            KnowledgeHub AI
                        </h1>

                        <p
                            className="
                text-xs
                text-muted-foreground
              "
                        >
                            Ask questions from your
                            organization documents
                        </p>
                    </div>
                </div>
            </header>

            {/* CHAT */}

            <main
                className="
          mx-auto flex w-full
          max-w-5xl flex-1
          flex-col px-6
        "
            >
                <div
                    className="
            flex-1 space-y-6
            overflow-y-auto
            py-8
          "
                >
                    {messages.length === 0 && (
                        <EmptyState />
                    )}

                    {messages.map(
                        (message) => (
                            <ChatMessageComponent
                                key={message.id}
                                message={message}
                            />
                        ),
                    )}

                    {loading && (
                        <div
                            className="
                flex items-center
                gap-2 text-sm
                text-muted-foreground
              "
                        >
                            <Loader2
                                className="
                  h-4 w-4 animate-spin
                "
                            />

                            Searching organization
                            knowledge...
                        </div>
                    )}
                </div>

                {/* ERROR */}

                {error && (
                    <div
                        className="
              mb-3 rounded-lg
              border border-destructive/40
              bg-destructive/10
              px-4 py-3
              text-sm text-destructive
            "
                    >
                        {error}
                    </div>
                )}

                {/* INPUT */}

                <form
                    onSubmit={handleSubmit}
                    className="
            sticky bottom-0
            bg-background
            pb-6 pt-3
          "
                >
                    <div
                        className="
              flex items-center
              gap-2 rounded-xl
              border bg-card
              p-2 shadow-sm
            "
                    >
                        <input
                            value={question}

                            onChange={(event) =>
                                setQuestion(
                                    event.target.value,
                                )
                            }

                            placeholder="
                Ask about a policy,
                SOP or document...
              "

                            className="
                flex-1 bg-transparent
                px-3 py-2
                text-sm outline-none
              "
                        />

                        <button
                            type="submit"

                            disabled={
                                loading ||
                                !question.trim()
                            }

                            className="
                flex h-10 w-10
                items-center justify-center
                rounded-lg bg-primary
                text-primary-foreground
                transition
                hover:opacity-90
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
                        >
                            {loading ? (
                                <Loader2
                                    className="
                    h-4 w-4
                    animate-spin
                  "
                                />
                            ) : (
                                <Send className="h-4 w-4" />
                            )}
                        </button>
                    </div>
                </form>
            </main>
        </div>
    );
}


function EmptyState() {

    return (
        <div
            className="
        flex min-h-[55vh]
        flex-col items-center
        justify-center text-center
      "
        >
            <div
                className="
          mb-4 flex h-14 w-14
          items-center justify-center
          rounded-2xl bg-muted
        "
            >
                <Sparkles className="h-6 w-6" />
            </div>

            <h2
                className="
          text-xl font-semibold
        "
            >
                Ask KnowledgeHub
            </h2>

            <p
                className="
          mt-2 max-w-md
          text-sm
          text-muted-foreground
        "
            >
                Ask questions about policies,
                procedures and other documents
                available to you.
            </p>
        </div>
    );
}