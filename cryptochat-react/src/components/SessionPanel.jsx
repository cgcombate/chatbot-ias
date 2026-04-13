export default function SessionPanel({
  mode,
  computedKey,
  onKeyChange,
  onImportKey,
  onExportSession,
}) {
  return (
    <aside className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
      <h2 className="text-sm font-bold">Session Keys & Logs</h2>
      <div className="mt-3 space-y-2">
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-2">
          <p className="text-xs text-slate-500">{mode === 'Asymmetric' ? 'Public key (simulated)' : 'Shared secret (shift)'}</p>
          <input
            value={computedKey}
            onChange={(e) => onKeyChange(e.target.value)}
            disabled={mode === 'Asymmetric'}
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm disabled:bg-slate-100"
          />
        </div>
        {['AES-256-CBC', 'RSA-2048', 'ChaCha20'].map((item) => (
          <div key={item} className="rounded-xl border border-slate-200 p-2">
            <p className="text-sm font-semibold">{item}</p>
            <p className="text-xs text-slate-500">Operational profile</p>
          </div>
        ))}
        <div className="h-28 rounded-xl border border-slate-200 bg-slate-50 p-2">
          <div className="h-full w-full rounded bg-gradient-to-r from-blue-100 to-blue-50" />
        </div>
      </div>
      <div className="mt-3 flex gap-2">
        <button onClick={onImportKey} className="rounded-xl border border-slate-200 px-3 py-2 text-xs font-semibold hover:bg-slate-100">
          Import Key
        </button>
        <button onClick={onExportSession} className="rounded-xl bg-brand px-3 py-2 text-xs font-semibold text-white hover:bg-sky-500">
          Export Session
        </button>
      </div>
    </aside>
  );
}
