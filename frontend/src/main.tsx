

import "./index.css";

import ReactDOM from "react-dom/client";
import { AuthProvider } from "./contexts/AuthContext";
import App from "./app/App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <AuthProvider>
    <App />
  </AuthProvider>
);