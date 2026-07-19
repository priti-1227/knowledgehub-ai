export function AuthFooter() {
  return (
    <div className="flex flex-col items-center w-full space-y-4">
      {/* Decorative Divider */}
      <div className="w-full h-px bg-gradient-to-r from-transparent via-neutral-200 to-transparent" />
      
      {/* Copyright Note */}
      <p className="text-xs font-semibold text-neutral-400 tracking-wider">
        &copy; 2026 KnowledgeHub AI
      </p>
    </div>
  );
}
