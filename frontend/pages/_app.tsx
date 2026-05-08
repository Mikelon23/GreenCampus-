import type { AppProps } from "next/app";
import { AuthProvider } from "../contexts/AuthContext";
import "leaflet/dist/leaflet.css";
import "../styles/globals.css";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
