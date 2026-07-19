interface Props {
  title: string;
  subtitle: string;
}

export function AuthHeader({ title, subtitle }: Props) {
  return (
    <div className="flex flex-col items-center text-center space-y-4">
      {/* Brand Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          KnowledgeHub AI
        </h1>
        <p className="text-[11px] font-bold tracking-widest text-neutral-500 uppercase">
          Enterprise Knowledge Assistant
        </p>
      </div>

      {/* Decorative Divider */}
      <div className="w-full h-px bg-gradient-to-r from-transparent via-neutral-200 to-transparent" />

      {/* Dynamic Welcome Message */}
      <div className="space-y-1">
        <h2 className="text-xl font-bold text-white tracking-tight">
          {title}
        </h2>
        <p className="text-xs text-neutral-500 font-medium">
          {subtitle}
        </p>
      </div>
    </div>
  );
}
