export default function ComposerBar({
  mode,
  setMode,
  message,
  setMessage,
  onSend,
  onClear,
}) {
  return (
    <div className="mt-4 flex flex-wrap items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 p-3 lg:gap-3 lg:p-4">
      <label className="text-xs font-semibold text-slate-500 lg:text-sm">Mode</label>
      <select
        value={mode}
        onChange={(e) => setMode(e.target.value)}
        className="rounded-2xl border border-slate-200 bg-white px-3 py-1.5 text-sm shadow-sm outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 lg:text-base"
      >
        <option>Symmetric</option>
        <option>Asymmetric</option>
      </select>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message to encrypt and send..."
        className="h-12 min-w-[260px] flex-1 rounded-xl border border-slate-200 p-2 text-sm outline-none focus:border-blue-400 lg:h-14 lg:text-base"
      />
      <button onClick={onSend} className="rounded-xl bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-sky-500 lg:px-5 lg:text-base">
        Send
      </button>
      <button onClick={onClear} className="rounded-xl border border-slate-200 px-3 py-2 text-sm hover:bg-slate-100 lg:px-4 lg:text-base">
        Clear
      </button>
    </div>
  );
}
