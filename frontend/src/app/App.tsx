import { useState } from "react";

interface RepoData {
  name: string;
  description: string;
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
  owner: {
    avatar_url: string;
    login: string;
  };
  html_url: string;
}

function App() {
  const [data, setData] = useState<RepoData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRepoInsights = async () => {
    setLoading(true);
    setError(null);
    try {
      // Native fetch API instead of Axios
      const response = await fetch("https://api.github.com/repos/priti-1227/knowledgehub-ai");
      
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
      }
      
      const result: RepoData = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background Decorative Glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-2xl w-full z-10">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            KnowledgeHub AI
          </h1>
          <p className="mt-3 text-slate-400 text-base md:text-lg">
            Smart knowledge base indexing & retrieval system.
          </p>
        </div>

        {/* Action Panel */}
        <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-2xl mb-8">
          <h2 className="text-xl font-semibold text-slate-200 mb-2">
            GitHub Repository Insights
          </h2>
          <p className="text-sm text-slate-400 mb-6">
            Demonstrating native <code className="bg-slate-950 text-indigo-300 px-2 py-0.5 rounded text-xs font-mono">fetch()</code> API to retrieve real-time project statistics from GitHub.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <input
              type="text"
              readOnly
              value="https://api.github.com/repos/priti-1227/knowledgehub-ai"
              className="flex-1 bg-slate-950/80 border border-slate-800 px-4 py-3 rounded-xl text-slate-400 text-sm font-mono focus:outline-none"
            />
            <button
              onClick={fetchRepoInsights}
              disabled={loading}
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 active:scale-95 text-white font-medium rounded-xl transition duration-200 flex items-center justify-center gap-2 shadow-lg disabled:opacity-75 disabled:pointer-events-none cursor-pointer"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  <span>Fetching...</span>
                </>
              ) : (
                <span>Fetch Insights</span>
              )}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-rose-950/30 border border-rose-900/50 rounded-xl text-rose-300 text-sm flex gap-3 items-center">
              <svg className="h-5 w-5 text-rose-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Fetched Data Layout */}
          {data && (
            <div className="mt-8 border-t border-slate-800/80 pt-6 transition-all duration-350">
              <div className="flex items-center gap-4 mb-6">
                <img
                  src={data.owner.avatar_url}
                  alt={data.owner.login}
                  className="w-12 h-12 rounded-full ring-2 ring-indigo-500/50"
                />
                <div>
                  <h3 className="font-bold text-lg text-white">
                    <a href={data.html_url} target="_blank" rel="noopener noreferrer" className="hover:text-indigo-400 transition-colors">
                      {data.name}
                    </a>
                  </h3>
                  <p className="text-xs text-slate-500 font-mono">Owner: {data.owner.login}</p>
                </div>
              </div>

              <p className="text-slate-300 text-sm leading-relaxed mb-6">
                {data.description || "No description provided for this repository."}
              </p>

              <div className="grid grid-cols-3 gap-4">
                <div className="bg-slate-950/50 border border-slate-800 p-4 rounded-xl text-center">
                  <div className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1">Stars</div>
                  <div className="text-2xl font-bold text-amber-400">{data.stargazers_count}</div>
                </div>
                <div className="bg-slate-950/50 border border-slate-800 p-4 rounded-xl text-center">
                  <div className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1">Forks</div>
                  <div className="text-2xl font-bold text-indigo-400">{data.forks_count}</div>
                </div>
                <div className="bg-slate-950/50 border border-slate-800 p-4 rounded-xl text-center">
                  <div className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-1">Issues</div>
                  <div className="text-2xl font-bold text-rose-450">{data.open_issues_count}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;