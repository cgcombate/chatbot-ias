export default function DecryptionView({
  decryptInput,
  setDecryptInput,
  decryptOutput,
  onDecrypt,
}) {
  return (
    <div className="space-y-3">
      <textarea
        value={decryptInput}
        onChange={(e) => setDecryptInput(e.target.value)}
        placeholder="Paste ciphertext here..."
        className="h-28 w-full rounded-2xl border border-slate-200 p-3 font-mono text-sm outline-none focus:border-blue-400"
      />
      <button onClick={onDecrypt} className="rounded-xl bg-brand px-3 py-2 text-sm font-semibold text-white hover:bg-sky-500">
        Decrypt
      </button>
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
        <p className="text-xs font-semibold text-slate-500">Output</p>
        <p className="mt-2 font-mono text-sm">{decryptOutput || 'Waiting for ciphertext...'}</p>
      </div>
    </div>
  );
}
