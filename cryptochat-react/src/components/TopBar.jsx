export default function TopBar({ tabs, activePath, onNavigate, onNewSession }) {
  return (
    <header className="flex items-center gap-3 bg-navy px-4 py-3 text-white shadow-soft">
      <div className="flex items-center gap-2 font-semibold">
        <span className="rounded-full bg-sky-400 px-2 py-0.5 text-xs">●</span>
        CryptoChat Lab
      </div>
      <div className="hidden gap-2 md:flex">
        {tabs.map((tab) => (
          <button
            key={tab.path}
            onClick={() => onNavigate(tab.path)}
            className={`rounded-xl px-3 py-1 text-xs font-semibold transition ${
              activePath === tab.path ? 'bg-sky-500' : 'bg-brand hover:bg-sky-500'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <button onClick={onNewSession} className="ml-auto rounded-xl bg-brand px-3 py-1 text-xs font-semibold hover:bg-sky-500">
        New Session
      </button>
    </header>
  );
}
