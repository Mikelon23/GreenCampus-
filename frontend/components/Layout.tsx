import Link from "next/link";
import { useRouter } from "next/router";
import { ReactNode, useMemo, useState } from "react";
import { useAuth } from "../contexts/AuthContext";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/forest", label: "Eco Forest" },
  { href: "/carbon", label: "Carbon Tracker" },
  { href: "/points", label: "Green Points" },
  { href: "/leaderboard", label: "Leaderboard" },
  { href: "/map", label: "Campus Map" },
  { href: "/hackathons", label: "GreenHack Hub" },
  { href: "/admin", label: "Admin Panel", adminOnly: true },
  { href: "/about", label: "About" }
];

export default function Layout({ children }: { children: ReactNode }) {
  const { user, logout, loading } = useAuth();
  const router = useRouter();
  const [mobileOpen, setMobileOpen] = useState(false);

  const visibleLinks = useMemo(
    () => links.filter((link) => !link.adminOnly || user?.role?.toLowerCase() === "admin"),
    [user]
  );

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.75),_transparent_35%),linear-gradient(145deg,_#edf6ef_0%,_#dcefe3_55%,_#f4f0e3_100%)]">
      <button
        type="button"
        onClick={() => setMobileOpen((value) => !value)}
        className="fixed left-4 top-4 z-40 rounded-xl bg-campus-800 px-4 py-2 text-sm font-semibold text-white shadow-lg md:hidden"
      >
        Menu
      </button>

      <aside
        className={`fixed inset-y-0 left-0 z-30 flex w-72 flex-col border-r border-campus-100 bg-campus-900 px-5 py-6 text-white shadow-2xl transition-transform duration-200 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
      >
        <div className="mb-6">
          <h1 className="font-display text-3xl font-bold tracking-tight text-white">GreenCampus+</h1>
          <p className="mt-2 text-sm text-campus-100/80">
            Sustainability intelligence for campus communities
          </p>
        </div>

        <nav className="flex-1 space-y-2 overflow-y-auto pr-1">
          {visibleLinks.map((link) => {
            const active = router.pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center justify-between rounded-2xl px-4 py-3 text-sm font-semibold transition ${
                  active
                    ? "bg-white text-campus-900 shadow-md"
                    : "bg-campus-800/50 text-campus-50 hover:bg-campus-700"
                }`}
              >
                <span>{link.label}</span>
                {active ? <span className="text-xs uppercase tracking-[0.2em]">Live</span> : null}
              </Link>
            );
          })}
        </nav>

        <div className="mt-6 rounded-2xl border border-campus-700 bg-campus-800/70 p-4">
          {!loading && user ? (
            <>
              <p className="text-xs uppercase tracking-[0.25em] text-campus-200">Signed in</p>
              <p className="mt-2 text-lg font-semibold text-white">{user.name}</p>
              <p className="text-sm capitalize text-campus-200">{user.role}</p>
              <button
                onClick={handleLogout}
                className="mt-4 w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-campus-900 transition hover:bg-campus-100"
              >
                Log out
              </button>
            </>
          ) : !loading ? (
            <div className="space-y-3">
              <p className="text-sm text-campus-100/80">
                Sign in to track energy, edit your submissions, and join the forest game.
              </p>
              <Link
                href="/login"
                className="block rounded-xl bg-white px-4 py-2 text-center text-sm font-semibold text-campus-900 transition hover:bg-campus-100"
              >
                Log in
              </Link>
              <Link
                href="/register"
                className="block rounded-xl border border-campus-500 px-4 py-2 text-center text-sm font-semibold text-white transition hover:bg-campus-700"
              >
                Sign up
              </Link>
            </div>
          ) : null}
        </div>
      </aside>

      <main className="min-h-screen px-4 pb-12 pt-20 md:ml-72 md:px-8 md:pt-8">
        <div className="mx-auto max-w-7xl">{children}</div>
      </main>
    </div>
  );
}
