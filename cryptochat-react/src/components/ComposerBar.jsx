export default function ComposerBar({
  mode,
  setMode,
  message,
  setMessage,
  onSend,
  onClear,
}) {
  return (
    <div className="mt-4 flex flex-wrap items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 p-3">
      <label className="text-xs font-semibold text-slate-500">Mode</label>
      <select value={mode} onChange={(e) => setMode(e.target.value)} className="rounded-xl border border-slate-200 bg-white px-2 py-1 text-sm">
        <option>Symmetric</option>
        <option>Asymmetric</option>
      </select>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message to encrypt and send..."
        className="h-12 min-w-[260px] flex-1 rounded-xl border border-slate-200 p-2 text-sm outline-none focus:border-blue-400"
      />
      <button onClick={onSend} className="rounded-xl bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-sky-500">
        Send
      </button>
      <button onClick={onClear} className="rounded-xl border border-slate-200 px-3 py-2 text-sm hover:bg-slate-100">
        Clear
      </button>
    </div>
  );
}
