"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { FileText, Plus } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface Note {
    id: number;
    title: string;
    created_at: string;
}

export default function NotesRoomPage() {
    const [notes, setNotes] = useState<Note[]>([]);
    const router = useRouter();

    useEffect(() => {
        api.get("/notes").then(res => setNotes(res.data));
    }, []);

    const createNote = async () => {
        const title = prompt("Note Title:");
        if (!title) return;

        const res = await api.post("/notes", { title });
        router.push(`/dashboard/notes/${res.data.id}`);
    };

    return (
        <div className="p-8 space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-white">Notes</h1>
                <button
                    onClick={createNote}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                    <Plus className="h-4 w-4" /> New Note
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {notes.map(note => (
                    <Link href={`/dashboard/notes/${note.id}`} key={note.id}>
                        <div className="p-6 bg-zinc-900 border border-zinc-800 rounded-xl hover:border-blue-500/50 transition cursor-pointer">
                            <FileText className="h-8 w-8 text-zinc-500 mb-4" />
                            <h3 className="font-bold text-white text-lg">{note.title}</h3>
                            <p className="text-xs text-zinc-500 mt-2">
                                {new Date(note.created_at).toLocaleDateString()}
                            </p>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
