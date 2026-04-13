export default function EncryptionModeView({ mode, setMode }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <p className="text-sm font-semibold">Choose encryption profile</p>
      <div className="mt-3 flex gap-3">
        {['Symmetric', 'Asymmetric'].map((item) => (
          <label key={item} className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm">
            <input type="radio" name="mode" checked={mode === item} onChange={() => setMode(item)} />
            {item}
          </label>
        ))}
      </div>
    </div>
  );
}
