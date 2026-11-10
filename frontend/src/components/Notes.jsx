import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  FileText, 
  Trash2, 
  CheckCircle2, 
  AlertCircle, 
  Loader2,
  FolderOpen
} from 'lucide-react';
import { api } from '../lib/api';

export default function Notes() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState(null);
  const fileInputRef = useRef(null);

  const loadNotes = async () => {
    setLoading(true);
    try {
      const data = await api.getNotes();
      setNotes(data.notes || []);
    } catch (err) {
      console.error(err);
      setMessage({ type: 'error', text: 'Failed to load notes from backend.' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNotes();
  }, []);

  const handleFileUpload = async (file) => {
    if (!file) return;

    const allowed = ['pdf', 'txt', 'md'];
    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowed.includes(ext)) {
      setMessage({ type: 'error', text: 'Only PDF, TXT, or MD files are supported.' });
      return;
    }

    setUploading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('subject', subject.trim() || 'General');

    try {
      await api.uploadNote(formData);
      setMessage({ type: 'success', text: `"${file.name}" uploaded, chunked & embedded!` });
      await loadNotes();
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Upload failed' });
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (id, filename) => {
    if (!confirm(`Delete "${filename}"? All associated vectors will be removed.`)) return;
    try {
      await api.deleteNote(id);
      setNotes(notes.filter((n) => n.id !== id));
      setMessage({ type: 'success', text: `Deleted "${filename}"` });
    } catch (err) {
      setMessage({ type: 'error', text: 'Delete failed.' });
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Class Notes & Documents</h2>
        <p className="text-sm text-slate-400">
          Upload PDF, TXT, or MD notes. They are split into ~500 token chunks and embedded for semantic retrieval.
        </p>
      </div>

      {message && (
        <div className={`p-4 rounded-xl flex items-center gap-3 text-sm font-medium ${
          message.type === 'success' 
            ? 'bg-emerald-950/50 text-emerald-300 border border-emerald-800'
            : 'bg-rose-950/50 text-rose-300 border border-rose-800'
        }`}>
          {message.type === 'success' ? <CheckCircle2 className="w-5 h-5 shrink-0" /> : <AlertCircle className="w-5 h-5 shrink-0" />}
          <span>{message.text}</span>
        </div>
      )}

      {/* Upload Box */}
      <div className="bg-[#0B0B14] border border-white/10 rounded-2xl p-6 shadow-xl space-y-5">
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Course / Subject
            </label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. Physics"
              className="px-3.5 py-2 text-sm rounded-xl border border-white/10 bg-[#121222] text-white focus:outline-none focus:ring-2 focus:ring-[#22E4FF] w-64 placeholder:text-slate-500"
            />
          </div>

          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => handleFileUpload(e.target.files[0])}
            accept=".pdf,.txt,.md"
            className="hidden"
          />
        </div>

        {/* Drag and Drop Zone */}
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files?.[0]) handleFileUpload(e.dataTransfer.files[0]);
          }}
          className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition ${
            uploading
              ? 'border-[#22E4FF] bg-[#22E4FF]/5 cursor-wait'
              : 'border-white/10 hover:border-[#B794FF] hover:bg-white/5'
          }`}
        >
          {uploading ? (
            <div className="space-y-3 flex flex-col items-center">
              <Loader2 className="w-8 h-8 text-[#22E4FF] animate-spin" />
              <p className="text-sm font-semibold text-[#22E4FF]">Extracting text & generating vector embeddings...</p>
              <p className="text-xs text-slate-400">Saving chunks to local MongoDB collection</p>
            </div>
          ) : (
            <>
              <div className="p-3 bg-[#B794FF]/10 rounded-full text-[#B794FF] mb-3">
                <Upload className="w-6 h-6" />
              </div>
              <p className="text-sm font-semibold text-slate-200">
                Click to upload or drag & drop class notes
              </p>
              <p className="text-xs text-slate-500 mt-1">PDF, TXT, or MD files (max 100 MB)</p>
            </>
          )}
        </div>
      </div>

      {/* Notes List */}
      <div className="bg-[#0B0B14] border border-white/10 rounded-2xl p-6 shadow-xl">
        <h3 className="font-semibold text-base mb-4 flex items-center gap-2 text-white">
          <FolderOpen className="w-4 h-4 text-[#22E4FF]" />
          Uploaded Notes ({notes.length})
        </h3>

        {loading ? (
          <div className="space-y-3">
            {[1, 2].map((i) => (
              <div key={i} className="h-16 bg-white/5 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : notes.length > 0 ? (
          <div className="divide-y divide-white/5">
            {notes.map((note) => (
              <div key={note.id} className="py-3.5 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="p-2.5 rounded-lg bg-[#5B21B6]/30 text-[#B794FF] shrink-0">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-white truncate">{note.filename}</p>
                    <div className="flex items-center gap-3 text-xs text-slate-400 mt-0.5">
                      <span className="px-2 py-0.5 rounded-md bg-white/10 font-medium text-[#22E4FF]">
                        {note.subject}
                      </span>
                      <span>{note.page_count} {note.page_count === 1 ? 'page' : 'pages'}</span>
                      <span>• {new Date(note.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => handleDelete(note.id, note.filename)}
                  className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-950/40 rounded-lg transition"
                  title="Delete note"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-10 text-slate-500 text-sm">
            No notes uploaded yet. Upload your first file above!
          </div>
        )}
      </div>
    </div>
  );
}
