"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import {
    Folder as FolderIcon,
    File as FileIcon,
    MoreVertical,
    Download,
    Trash2,
    Upload,
    FolderPlus,
    ArrowLeft
} from "lucide-react";
import { useRouter } from "next/navigation";

interface FileItem {
    id: number;
    name: string;
    size: number;
    content_type: string;
    created_at: string;
    is_folder: boolean;
}

export default function FileRoomPage() {
    const [files, setFiles] = useState<FileItem[]>([]);
    const [currentFolderId, setCurrentFolderId] = useState<number | null>(null);
    const [folderHistory, setFolderHistory] = useState<number[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchFiles = async (folderId: number | null) => {
        setLoading(true);
        try {
            const res = await api.get(`/files/list`, {
                params: { folder_id: folderId }
            });
            setFiles(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFiles(currentFolderId);
    }, [currentFolderId]);

    const handleFolderClick = (id: number) => {
        setFolderHistory([...folderHistory, currentFolderId!]);
        setCurrentFolderId(id);
    };

    const handleBack = () => {
        if (folderHistory.length === 0) return;
        const prev = folderHistory[folderHistory.length - 1]; // Can be null
        setFolderHistory(folderHistory.slice(0, -1));
        setCurrentFolderId(prev);
    };

    const handleCreateFolder = async () => {
        const name = prompt("Enter folder name:");
        if (!name) return;
        try {
            await api.post("/files/folders", { name, parent_id: currentFolderId });
            fetchFiles(currentFolderId);
        } catch (err) {
            alert("Failed to create folder");
        }
    };

    return (
        <div className="p-8 space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    {folderHistory.length > 0 && (
                        <button onClick={handleBack} className="p-2 hover:bg-zinc-800 rounded-lg text-white">
                            <ArrowLeft className="h-5 w-5" />
                        </button>
                    )}
                    <h1 className="text-2xl font-bold text-white">Files</h1>
                </div>

                <div className="flex gap-4">
                    <button
                        onClick={handleCreateFolder}
                        className="flex items-center gap-2 px-4 py-2 bg-zinc-800 text-white rounded-lg hover:bg-zinc-700 transition"
                    >
                        <FolderPlus className="h-4 w-4" /> New Folder
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg hover:bg-zinc-200 transition font-medium">
                        <Upload className="h-4 w-4" /> Upload
                    </button>
                </div>
            </div>

            {loading ? (
                <div className="text-zinc-500">Loading...</div>
            ) : (
                <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-zinc-950 border-b border-zinc-800">
                            <tr>
                                <th className="p-4 text-xs font-medium text-zinc-400 uppercase">Name</th>
                                <th className="p-4 text-xs font-medium text-zinc-400 uppercase">Size</th>
                                <th className="p-4 text-xs font-medium text-zinc-400 uppercase">Type</th>
                                <th className="p-4 text-xs font-medium text-zinc-400 uppercase w-10"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {files.length === 0 && (
                                <tr>
                                    <td colSpan={4} className="p-8 text-center text-zinc-500">This folder is empty.</td>
                                </tr>
                            )}
                            {files.map((file) => (
                                <tr
                                    key={file.id}
                                    className="border-b border-zinc-800/50 last:border-0 hover:bg-zinc-800/50 transition cursor-pointer"
                                    onClick={() => file.is_folder && handleFolderClick(file.id)}
                                >
                                    <td className="p-4 flex items-center gap-3">
                                        {file.is_folder ? (
                                            <FolderIcon className="h-5 w-5 text-yellow-500 fill-yellow-500/20" />
                                        ) : (
                                            <FileIcon className="h-5 w-5 text-blue-500" />
                                        )}
                                        <span className="text-white font-medium">{file.name}</span>
                                    </td>
                                    <td className="p-4 text-zinc-400 text-sm">{file.is_folder ? "-" : `${(file.size / 1024 / 1024).toFixed(2)} MB`}</td>
                                    <td className="p-4 text-zinc-400 text-sm">{file.content_type}</td>
                                    <td className="p-4">
                                        <button className="p-2 hover:bg-zinc-800 rounded-full text-zinc-400 hover:text-white">
                                            <MoreVertical className="h-4 w-4" />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
