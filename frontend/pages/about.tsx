import Layout from "../components/Layout";
import SectionHeader from "../components/SectionHeader";
import Link from "next/link";

export default function AboutPage() {
  return (
    <Layout>
      <SectionHeader
        title="About GreenCampus+"
        subtitle="Driving sustainability through intelligence and gamification"
      />
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Mission */}
        <div className="rounded-3xl bg-white/90 p-8 shadow-sm lg:col-span-2">
          <h2 className="mb-4 font-display text-2xl font-semibold text-campus-800">
            Our Mission
          </h2>
          <p className="mb-4 text-campus-700 leading-relaxed">
            GreenCampus+ is an integrated platform designed to monitor campus environmental
            metrics and motivate students, faculty, and staff to adopt sustainable habits.
            We combine real-time IoT sensor data (temperature, CO₂, energy) with an
            interactive gamification system.
          </p>
          <p className="text-campus-700 leading-relaxed">
            By making invisible environmental data visible and rewarding positive actions,
            we aim to create a lasting culture of sustainability across our institution.
          </p>
        </div>

        {/* How Gamification Works */}
        <div className="rounded-3xl bg-campus-700 p-8 text-white shadow-sm lg:col-span-1">
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            How to Earn Green Points
          </h2>
          <ul className="space-y-3 text-sm text-campus-50 opacity-90">
            <li className="flex items-center gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-campus-600 font-bold">1</span>
              Perform eco-actions (e.g., recycling, cycling to campus).
            </li>
            <li className="flex items-center gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-campus-600 font-bold">2</span>
              Log your actions in the <Link href="/points" className="underline hover:text-white">Green Points</Link> section.
            </li>
            <li className="flex items-center gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-campus-600 font-bold">3</span>
              Earn points instantly and climb the Leaderboard.
            </li>
            <li className="flex items-center gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-campus-600 font-bold">4</span>
              Unlock exclusive badges for milestones!
            </li>
          </ul>
        </div>
      </div>

      <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* Achievement Levels */}
        <div className="rounded-3xl bg-white/90 p-6 shadow-sm lg:col-span-2">
          <h3 className="mb-4 font-display text-xl font-semibold text-campus-800">
            Achievement Levels
          </h3>
          <div className="space-y-3">
            {[
              { level: "1", name: "Beginner", range: "0 - 100 pts" },
              { level: "2", name: "Eco Supporter", range: "100 - 300 pts" },
              { level: "3", name: "Sustainability Advocate", range: "300 - 700 pts" },
              { level: "4", name: "Green Leader", range: "700+ pts" },
            ].map((lvl) => (
              <div key={lvl.level} className="flex items-center justify-between rounded-xl bg-campus-50 p-3">
                <div className="flex items-center gap-3">
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-campus-800 font-bold text-white">
                    {lvl.level}
                  </span>
                  <span className="font-semibold text-campus-800">{lvl.name}</span>
                </div>
                <span className="text-sm text-campus-600">{lvl.range}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Hackathons Info */}
        <div className="rounded-3xl bg-white/90 p-6 shadow-sm lg:col-span-2">
          <h3 className="mb-4 font-display text-xl font-semibold text-campus-800">
            GreenHack Hub
          </h3>
          <p className="mb-4 text-sm text-campus-700 leading-relaxed">
            Ready to make a bigger impact? Participate in our periodic sustainability
            hackathons. Work with teams to design innovative solutions for the campus
            infrastructure, reduce waste, and improve biodiversity.
          </p>
          <div className="mt-auto">
            <Link
              href="/hackathons"
              className="inline-block rounded-xl bg-campus-100 px-5 py-2.5 text-sm font-semibold text-campus-800 transition hover:bg-campus-200"
            >
              View Active Hackathons
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
