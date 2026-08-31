import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import {
    QueryClient,
    QueryClientProvider,
} from "@tanstack/react-query";

import App from "./App";
import GlobalStyle from "./styles/GlobalStyle";


const queryClient = new QueryClient();


createRoot(
    document.getElementById("root")
).render(
    <StrictMode>
        <QueryClientProvider client={queryClient}>
            <GlobalStyle />

            <App />
        </QueryClientProvider>
    </StrictMode>
);