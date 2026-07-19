import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

export default function AuthCard({ children }: Props) {
  return (
    <div
      className="
        w-full
        max-w-md
        rounded-2xl
        border
        
        p-8
        shadow-lg
      "
    >
      {children}
    </div>
  );
}
