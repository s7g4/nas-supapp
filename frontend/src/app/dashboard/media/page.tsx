"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Play, PlaySquare } from "lucide-react";
import Link from "next/link";

interface MediaItem {
    id: number;
    name: string;
    size: number;
    created_at: string;
}

export default function MediaRoomPage() {
    const [videos, setVideos] = useState<MediaItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMedia = async () => {
            try {
                const res = await api.get("/media/list");
                setVideos(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchMedia();
    }, []);

    return (
        <div className="p-8 space-y-6">
            <div className="flex items-center gap-4">
                <h1 className="text-2xl font-bold text-white">Media Room</h1>
                <span className="bg-zinc-800 text-zinc-400 text-xs px-2 py-1 rounded-full">{videos.length} Videos</span>
            </div>

            {loading ? (
                <div className="text-zinc-500">Loading library...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {videos.length === 0 && (
                        <div className="col-span-full text-center py-12 text-zinc-500 border border-dashed border-zinc-800 rounded-xl">
                            No videos found in your storage.
                        </div>
                    )}
                    {videos.map((video) => (
                        <Link href={`/dashboard/media/${video.id}`} key={video.id}>
                            <div className="group bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden hover:border-blue-500/50 transition cursor-pointer">
                                {/* Thumbnail Fallback */}
                                <div className="aspect-video bg-zinc-950 flex items-center justify-center relative">
                                    <PlaySquare className="h-12 w-12 text-zinc-700 group-hover:text-blue-500 transition" />
                                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition">
                                        <Play className="h-12 w-12 text-white fill-white" />
                                    </div>
                                </div>
                                <div className="p-4">
                                    <h3 className="font-medium text-white truncate" title={video.name}>{video.name}</h3>
                                    <p className="text-sm text-zinc-500 mt-1">{(video.size / 1024 / 1024).toFixed(2)} MB</p>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    );
}
