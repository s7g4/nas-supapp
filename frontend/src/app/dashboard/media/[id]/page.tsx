"use client";

import { useParams } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useRef, useEffect } from "react";

export default function VideoPlayerPage() {
    const params = useParams();
    const videoRef = useRef<HTMLVideoElement>(null);
    const videoSrc = `${process.env.NEXT_PUBLIC_API_URL}/media/stream/${params.id}`;

    return (
        <div className="p-8 h-full flex flex-col">
            <div className="flex items-center gap-4 mb-6">
                <Link href="/dashboard/media" className="p-2 hover:bg-zinc-800 rounded-lg text-white">
                    <ArrowLeft className="h-5 w-5" />
                </Link>
                <h1 className="text-xl font-bold text-white">Now Playing</h1>
                <button
                    onClick={() => {
                        fetch(`${process.env.NEXT_PUBLIC_API_URL}/media/transcode/${params.id}`, {
                            method: 'POST',
                            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                        }).then(() => alert("Transcoding started! Check back in a minute."))
                    }}
                    className="ml-auto px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm"
                >
                    Optimize for Streaming
                </button>
            </div>

            <div className="flex-1 bg-black rounded-2xl overflow-hidden shadow-2xl border border-zinc-800">
                {/* Native Video Player */}
                <video
                    ref={videoRef}
                    className="w-full h-full object-contain"
                    controls
                    autoPlay
                    crossOrigin="anonymous"
                >
                    <source src={videoSrc} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    );
}
