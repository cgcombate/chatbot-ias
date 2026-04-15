import { useEffect, useMemo, useState } from 'react';

export default function SessionPanel({
  mode,
  computedKey,
  logs,
  lastActivityAt,
  onKeyChange,
  onImportKey,
  onExportSession,
}) {
  const totalEncrypted = logs.network.length;
  const totalDecrypted = logs.recipient.length;
  const latestCipher = logs.network[0] ?? 'No ciphertext generated yet.';
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 30000);
    return () => window.clearInterval(timer);
  }, []);

  const lastActivityLabel = useMemo(() => {
    if (!lastActivityAt) return 'No activity yet';
    const secondsAgo = Math.max(0, Math.floor((now - lastActivityAt) / 1000));
    if (secondsAgo < 5) return 'Just now';
    if (secondsAgo < 60) return `${secondsAgo}s ago`;
    const minutesAgo = Math.floor(secondsAgo / 60);
    if (minutesAgo < 60) return `${minutesAgo}m ago`;
    const hoursAgo = Math.floor(minutesAgo / 60);
    if (hoursAgo < 24) return `${hoursAgo}h ago`;
    const daysAgo = Math.floor(hoursAgo / 24);
    return `${daysAgo}d ago`;
  }, [lastActivityAt, now]);

  return (
    <aside className="w-full rounded-2xl border border-slate-200 bg-white p-4 shadow-soft lg:p-6">
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

      <div className="mt-3 space-y-2 lg:space-y-3">
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 lg:p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 lg:text-sm">Live Session Stats</p>
          <div className="mt-2 grid grid-cols-2 gap-2 lg:gap-3">
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Encrypted</p>
              <p className="text-sm font-semibold text-slate-800 lg:text-base">{totalEncrypted}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Decrypted</p>
              <p className="text-sm font-semibold text-slate-800 lg:text-base">{totalDecrypted}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Mode</p>
              <p className="text-sm font-semibold text-slate-800 lg:text-base">{mode}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-2">
              <p className="text-[11px] uppercase tracking-wide text-slate-500">Last Activity</p>
              <p className="text-sm font-semibold text-slate-800 lg:text-base">{lastActivityLabel}</p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-indigo-50 p-3 lg:p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600 lg:text-sm">Latest Ciphertext</p>
          <p className="mt-1 break-all font-mono text-xs text-indigo-900 lg:text-sm">{latestCipher}</p>
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
