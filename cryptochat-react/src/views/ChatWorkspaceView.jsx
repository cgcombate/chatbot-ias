const cards = [
  {
    title: 'SecureBot',
    key: 'network',
    tone: 'border-violet-200 bg-violet-50 text-violet-900',
  },
  {
    title: 'You',
    key: 'recipient',
    tone: 'border-emerald-200 bg-emerald-50 text-emerald-900',
  },
  {
    title: 'You • Preview',
    key: 'preview',
    tone: 'border-sky-200 bg-sky-50 text-sky-900',
  },
];

export default function ChatWorkspaceView({ logs }) {
  return (
    <div className="space-y-3 lg:space-y-4">
      {cards.map((card) => (
        <div key={card.key} className={`rounded-2xl border p-3 lg:p-4 ${card.tone}`}>
          <p className="mb-2 text-sm font-semibold lg:text-base">{card.title}</p>
          <div className="space-y-1 font-mono text-xs lg:text-sm">
            {(logs[card.key].length ? logs[card.key] : ['No messages yet.']).map((item, idx) => (
              <p key={`${card.key}-${idx}`}>{item}</p>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
