export default function SessionPanel({
  mode,
  computedKey,
  logs,
  incoming,
  onKeyChange,
  onImportKey,
  onExportSession,
}) {
  const totalEncrypted = logs.network.length;
  const totalDecrypted = logs.recipient.length;
  const queueSize = incoming.length;
  const latestCipher = logs.network[0] ?? 'No ciphertext generated yet.';

  return (
    <aside className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <h2 className="pt-1 text-sm font-bold">Session Keys & Logs</h2>
        <div className="w-full sm:max-w-[300px] rounded-xl border border-slate-200 bg-slate-50 p-2">
          <p className="text-xs text-slate-500">
            {mode === 'Asymmetric' ? 'Public key (simulated)' : 'Shared secret (shift)'}
          </p>
          <input
            value={computedKey}
            onChange={(e) => onKeyChange(e.target.value)}
            disabled={mode === 'Asymmetric'}
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm disabled:bg-slate-100"
          />
        </div>
      </div>

      <div className="mt-3 space-y-2">
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Live Session Stats</p>
          <div className="mt-2 grid grid-cols-2 gap-2">
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Encrypted</p>
              <p className="text-sm font-semibold text-slate-800">{totalEncrypted}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Decrypted</p>
              <p className="text-sm font-semibold text-slate-800">{totalDecrypted}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Incoming Queue</p>
              <p className="text-sm font-semibold text-slate-800">{queueSize}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Mode</p>
              <p className="text-sm font-semibold text-slate-800">{mode}</p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-indigo-50 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">Latest Ciphertext</p>
          <p className="mt-1 break-all font-mono text-xs text-indigo-900">{latestCipher}</p>
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
