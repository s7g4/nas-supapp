import {
    FolderOpen,
    PlaySquare,
    HardDrive,
    Clock
} from "lucide-react";

export default function DashboardPage() {
    return (
        <main className="p-8 space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-white">Dashboard</h1>
                <p className="text-zinc-400 mt-1">Overview of your local cloud system.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Storage"
                    value="450 GB / 2 TB"
                    icon={<HardDrive className="h-6 w-6 text-blue-500" />}
                />
                <StatCard
                    title="Active Files"
                    value="1,240"
                    icon={<FolderOpen className="h-6 w-6 text-yellow-500" />}
                />
                <StatCard
                    title="Media Library"
                    value="320 Hours"
                    icon={<PlaySquare className="h-6 w-6 text-purple-500" />}
                />
                <StatCard
                    title="System Uptime"
                    value="12d 4h"
                    icon={<Clock className="h-6 w-6 text-green-500" />}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                    <h3 className="font-semibold text-white mb-4">Recent Activity</h3>
                    <div className="space-y-4">
                        {/* Mock activity items */}
                        <ActivityItem action="Uploaded" file="project-specs.pdf" time="2 mins ago" />
                        <ActivityItem action="Downloaded" file="vacation-video.mp4" time="1 hour ago" />
                        <ActivityItem action="Modified" file="notes.md" time="3 hours ago" />
                    </div>
                </div>

                <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                    <h3 className="font-semibold text-white mb-4">Quick Actions</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <ActionButton label="Upload File" />
                        <ActionButton label="Create Folder" />
                        <ActionButton label="Start Stream" />
                        <ActionButton label="New Note" />
                    </div>
                </div>
            </div>
        </main>
    );
}

function StatCard({ title, value, icon }: { title: string, value: string, icon: any }) {
    return (
        <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-xl flex items-center justify-between">
            <div>
                <p className="text-zinc-400 text-sm font-medium">{title}</p>
                <p className="text-2xl font-bold text-white mt-1">{value}</p>
            </div>
            <div className="p-3 bg-zinc-950 rounded-lg border border-zinc-800">
                {icon}
            </div>
        </div>
    )
}

function ActivityItem({ action, file, time }: { action: string, file: string, time: string }) {
    return (
        <div className="flex items-center justify-between py-2 border-b border-zinc-800/50 last:border-0">
            <div className="flex items-center gap-3">
                <div className="h-2 w-2 rounded-full bg-blue-500" />
                <div>
                    <p className="text-sm font-medium text-white">{action} <span className="text-zinc-400">{file}</span></p>
                </div>
            </div>
            <span className="text-xs text-zinc-500">{time}</span>
        </div>
    )
}

function ActionButton({ label }: { label: string }) {
    return (
        <button className="p-4 bg-zinc-950 border border-zinc-800 hover:bg-zinc-800 rounded-lg text-sm font-medium text-zinc-300 hover:text-white transition">
            {label}
        </button>
    )
}
