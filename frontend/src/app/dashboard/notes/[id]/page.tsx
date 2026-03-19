"use client";

import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { Save, Loader2 } from "lucide-react";

export default function NoteEditorPage() {
    const params = useParams();
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");
    const [saving, setSaving] = useState(false);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        // Basic Fetch
        api.get(`/notes/${params.id}`).then(res => {
            setTitle(res.data.title);
            setContent(res.data.content);
        });

        // WebSocket Init
        const token = localStorage.getItem("token");
        if (!token) return;

        const wsUrl = process.env.NEXT_PUBLIC_API_URL?.replace("http", "ws") || "ws://localhost:8000";
        const socket = new WebSocket(`${wsUrl}/notes/ws/${params.id}?token=${token}`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // Naive update: just replace content if it's different
            // In prod, use Yjs/CRDT
            if (data.content && data.content !== content) {
                setContent(data.content);
            }
        };

        ws.current = socket;
        return () => socket.close();
    }, [params.id]);

    const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newContent = e.target.value;
        setContent(newContent);
        // Broadcast change
        ws.current?.send(JSON.stringify({ content: newContent }));
    };

    const saveNote = async () => {
        setSaving(true);
        await api.put(`/notes/${params.id}`, { content });
        setSaving(false);
    };

    return (
        <div className="h-full flex flex-col">
            <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900">
                <h1 className="text-xl font-bold text-white">{title}</h1>
                <button
                    onClick={saveNote}
                    disabled={saving}
                    className="flex items-center gap-2 px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-sm transition"
                >
                    {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                    Save
                </button>
            </div>
            <div className="flex-1 bg-zinc-950 p-4">
                <textarea
                    className="w-full h-full bg-transparent text-white resize-none focus:outline-none font-mono"
                    value={content}
                    onChange={handleContentChange}
                    placeholder="Start typing..."
                />
            </div>
        </div>
    );
}
