import Link from "next/link";
import { ArrowRight, Shield, Zap, HardDrive } from "lucide-react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-zinc-950 text-white p-6">
      <div className="max-w-3xl text-center space-y-6">
        <div className="flex justify-center space-x-4 mb-4">
          <div className="p-3 bg-zinc-900 rounded-full border border-zinc-800">
            <HardDrive className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <h1 className="text-5xl font-bold tracking-tight bg-gradient-to-r from-white to-zinc-500 bg-clip-text text-transparent">
          NAS Super-App
        </h1>

        <p className="text-zinc-400 text-xl">
          Your self-hosted, local-first digital cloud. Blazing fast, secure, and modular.
        </p>

        <div className="flex justify-center gap-4 pt-6">
          <Link href="/auth/login" className="px-6 py-3 bg-white text-black font-medium rounded-lg hover:bg-zinc-200 transition flex items-center gap-2">
            Get Started <ArrowRight className="h-4 w-4" />
          </Link>
          <Link href="https://github.com/s7g4/nas-supapp" className="px-6 py-3 bg-zinc-900 border border-zinc-800 text-white font-medium rounded-lg hover:bg-zinc-800 transition">
            View Source
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12 text-left">
          <FeatureCard
            icon={<Zap className="h-6 w-6 text-yellow-500" />}
            title="Fast Transfer"
            desc="QUIC-powered engine for saturation-level LAN speeds."
          />
          <FeatureCard
            icon={<Shield className="h-6 w-6 text-green-500" />}
            title="Secure Core"
            desc="Microkernel architecture with JWT-based isolation."
          />
          <FeatureCard
            icon={<HardDrive className="h-6 w-6 text-blue-500" />}
            title="Modular Rooms"
            desc="Pluggable modules for Files, Media, Chat, and AI."
          />
        </div>
      </div>
    </main>
  );
}

function FeatureCard({ icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="p-6 bg-zinc-900/50 border border-zinc-800 rounded-xl space-y-3">
      {icon}
      <h3 className="font-semibold text-white">{title}</h3>
      <p className="text-sm text-zinc-400">{desc}</p>
    </div>
  )
}
