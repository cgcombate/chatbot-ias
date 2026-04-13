export default function Sidebar({ tabs, activePath, onNavigate }) {
  return (
    <aside className="rounded-2xl border border-slate-200 bg-white p-3 shadow-soft">
      <p className="mb-3 text-xs font-semibold text-slate-500">Sections</p>
      <div className="space-y-1">
        {tabs.map((tab) => (
          <button
            key={tab.path}
            onClick={() => onNavigate(tab.path)}
            className={`w-full rounded-xl px-3 py-2 text-left text-sm ${
              activePath === tab.path ? 'bg-blue-100 text-blue-700' : 'hover:bg-slate-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </aside>
  );
}
