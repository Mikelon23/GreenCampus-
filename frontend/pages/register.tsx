import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import { api } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.register({ name, email, password, role });
      login(response.access_token, response.user);
      router.push("/");
    } catch (err: any) {
      setError(err.message || "Failed to register account");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="mx-auto max-w-md pt-12">
        <div className="rounded-3xl bg-white/90 p-8 shadow-sm">
          <SectionHeader
            title="Create an account"
            subtitle="Join GreenCampus+ to track your impact"
          />
          
          {error && (
            <div className="mb-6 rounded-xl bg-red-50 p-4 text-sm text-red-800">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-campus-700">
                Full Name
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-xl border-campus-200 bg-campus-50 px-4 py-2.5 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                placeholder="Jane Doe"
              />
            </div>
            
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
                Role
              </label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full appearance-none rounded-xl border-campus-200 bg-campus-50 px-4 py-2.5 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
              >
                <option value="student">Student</option>
                <option value="faculty">Faculty</option>
                <option value="researcher">Researcher</option>
              </select>
            </div>
            
            <div>
              <label className="mb-1 block text-sm font-medium text-campus-700">
                Password
              </label>
              <input
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-xl border-campus-200 bg-campus-50 px-4 py-2.5 outline-none transition focus:border-campus-400 focus:bg-white focus:ring-2 focus:ring-campus-400/20"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full rounded-xl bg-campus-700 py-3 font-semibold text-white shadow-sm transition hover:bg-campus-800 disabled:opacity-50"
            >
              {loading ? "Creating account..." : "Sign up"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-campus-600">
            Already have an account?{" "}
            <Link href="/login" className="font-semibold text-campus-800 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}
