import { RouterProvider } from "react-router-dom";
import { router } from "@/app/router";

import "./index.css";

import ReactDOM from "react-dom/client";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <RouterProvider router={router} />
);