export default function ReceivePaneView({ incoming, onSelectIncoming }) {
  return (
    <div className="space-y-2">
      <p className="text-sm text-slate-500">Captured encrypted payloads.</p>
      <div className="max-h-80 space-y-2 overflow-auto rounded-2xl border border-slate-200 bg-slate-50 p-2">
        {(incoming.length ? incoming : ['No incoming messages yet.']).map((item, idx) => (
          <button
            key={`${item}-${idx}`}
            onClick={() => onSelectIncoming(item)}
            className="w-full rounded-xl border border-slate-200 bg-white p-2 text-left font-mono text-xs hover:border-blue-300"
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}
