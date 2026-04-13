const cards = [
  { title: 'SecureBot', key: 'network', tone: 'bg-slate-100' },
  { title: 'You', key: 'recipient', tone: 'bg-white' },
  { title: 'You • Preview', key: 'preview', tone: 'bg-blue-50' },
];

export default function ChatWorkspaceView({ logs }) {
  return (
    <div className="space-y-3">
      {cards.map((card) => (
        <div key={card.key} className={`rounded-2xl border border-slate-200 p-3 ${card.tone}`}>
          <p className="mb-2 text-sm font-semibold">{card.title}</p>
          <div className="space-y-1 font-mono text-xs text-slate-700">
            {(logs[card.key].length ? logs[card.key] : ['No messages yet.']).map((item, idx) => (
              <p key={`${card.key}-${idx}`}>{item}</p>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
