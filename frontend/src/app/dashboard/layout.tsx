"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    FolderOpen,
    PlaySquare,
    MessageSquare,
    Settings,
    LogOut,
    HardDrive
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
    { name: 'Overview', href: '/dashboard', icon: LayoutDashboard },
    { name: 'My Files', href: '/dashboard/files', icon: FolderOpen },
    { name: 'Media Room', href: '/dashboard/media', icon: PlaySquare },
    { name: 'Chat Room', href: '/dashboard/chat', icon: MessageSquare },
    { name: 'Stream Room', href: '/dashboard/stream', icon: PlaySquare },
    { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const pathname = usePathname();

    return (
        <div className="flex h-screen bg-zinc-950 text-white">
            {/* Sidebar */}
            <div className="w-64 border-r border-zinc-800 bg-zinc-900 flex flex-col">
                <div className="p-6 border-b border-zinc-800 flex items-center gap-3">
                    <HardDrive className="h-6 w-6 text-blue-500" />
                    <span className="font-bold text-lg">NAS Cloud</span>
                </div>

                <nav className="flex-1 p-4 space-y-1">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                                    isActive
                                        ? "bg-zinc-800 text-white"
                                        : "text-zinc-400 hover:text-white hover:bg-zinc-800/50"
                                )}
                            >
                                <item.icon className="h-5 w-5" />
                                {item.name}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-zinc-800">
                    <button
                        onClick={() => {
                            localStorage.removeItem("token");
                            window.location.href = "/auth/login";
                        }}
                        className="flex items-center gap-3 px-3 py-2 w-full text-zinc-400 hover:text-red-400 hover:bg-zinc-800/50 rounded-lg text-sm font-medium transition"
                    >
                        <LogOut className="h-5 w-5" />
                        Sign Out
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 overflow-auto">
                {children}
            </div>
        </div>
    );
}
