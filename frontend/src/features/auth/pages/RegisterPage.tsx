import AuthCard from "../components/AuthCard";
import { AuthHeader } from "../components/AuthHeader";
import { RegisterForm } from "../components/RegisterForm";
import { AuthFooter } from "../components/AuthFooter";

export default function RegisterPage() {
  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-[#0B0A0F] px-4 py-12 overflow-hidden">
      {/* Background Decorative Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-900/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/20 blur-[120px] pointer-events-none" />
      
      {/* Grid Pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f1f2e_1px,transparent_1px),linear-gradient(to_bottom,#1f1f2e_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-30 pointer-events-none" />

      {/* Main card container */}
      <div className="w-full max-w-md relative z-10 animate-fade-in">
        <AuthCard>
          <div className="flex flex-col space-y-6">
            {/* Dynamic Header */}
            <AuthHeader 
              title="Create your account" 
              subtitle="Start using KnowledgeHub AI" 
            />
            
            {/* Form */}
            <RegisterForm />
            
            {/* Divider */}
            <div className="relative flex items-center">
              <div className="flex-grow border-t border-neutral-200"></div>
              <span className="flex-shrink mx-4 text-[10px] font-bold text-neutral-400 uppercase tracking-widest">
                Protected Session
              </span>
              <div className="flex-grow border-t border-neutral-200"></div>
            </div>

            {/* Footer */}
            <AuthFooter />
          </div>
        </AuthCard>
      </div>
    </div>
  );
}
