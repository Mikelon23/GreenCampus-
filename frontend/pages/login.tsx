import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { api } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.login({ email, password });
      login(response.access_token, response.user);
      router.push("/");
    } catch (err: any) {
      setError(err.message || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="mx-auto max-w-md pt-12">
        <div className="rounded-3xl bg-white/90 p-8 shadow-sm">
          <SectionHeader
            title="Welcome back"
            subtitle="Sign in to your GreenCampus+ account"
          />
          
          {error && (
            <div className="mb-6 rounded-xl bg-red-50 p-4 text-sm text-red-800">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="mb-1 block text-sm font-medium text-campus-700">
                Email address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-xl border-campus-200 bg-campus-50 px-4 py-2.5 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                placeholder="student@campus.edu"
              />
            </div>
            
            <div>
              <label className="mb-1 block text-sm font-medium text-campus-700">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-xl border-campus-200 bg-campus-50 px-4 py-2.5 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 w-full rounded-xl bg-campus-700 py-3 font-semibold text-white shadow-sm transition hover:bg-campus-800 disabled:opacity-50"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-campus-600">
            Don't have an account?{" "}
            <Link href="/register" className="font-semibold text-campus-800 hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}
