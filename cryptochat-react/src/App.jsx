import { useMemo, useState } from 'react';
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import ComposerBar from './components/ComposerBar';
import SessionPanel from './components/SessionPanel';
import TopBar from './components/TopBar';
import { tabLabelByPath, tabs } from './constants/tabs';
import { caesar, fromBase64, toBase64 } from './lib/crypto';
import ChatWorkspaceView from './views/ChatWorkspaceView';
import DecryptionView from './views/DecryptionView';
import ReceivePaneView from './views/ReceivePaneView';

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const [mode, setMode] = useState('Symmetric');
  const [message, setMessage] = useState('');
  const [decryptInput, setDecryptInput] = useState('');
  const [decryptOutput, setDecryptOutput] = useState('');
  const [status, setStatus] = useState('Ready');
  const [keyInput, setKeyInput] = useState('3');
  const [logs, setLogs] = useState({ network: [], recipient: [], preview: [] });
  const [incoming, setIncoming] = useState([]);

  const computedKey = useMemo(
    () => (mode === 'Asymmetric' ? 'RSA_PUB_8821' : keyInput),
    [mode, keyInput],
  );
  const activePath = tabLabelByPath[location.pathname] ? location.pathname : '/';
  const activeLabel = tabLabelByPath[activePath];

  const clearHistory = () => {
    setLogs({ network: [], recipient: [], preview: [] });
    setIncoming([]);
    setStatus('History cleared');
  };

  const newSession = () => {
    clearHistory();
    setMessage('');
    setDecryptInput('');
    setDecryptOutput('');
    setStatus('New session started');
  };

  const processMessage = () => {
    const raw = message.trim();
    if (!raw) return;

    try {
      let encrypted = '';
      let decrypted = '';
      let protocol = '';
      if (mode === 'Symmetric') {
        const key = Number.parseInt(keyInput, 10);
        if (Number.isNaN(key)) throw new Error('Symmetric key must be a number.');
        encrypted = caesar(raw, key);
        decrypted = caesar(encrypted, key, true);
        protocol = `AES-SIM key:${key}`;
      } else {
        encrypted = toBase64(raw);
        decrypted = fromBase64(encrypted);
        protocol = 'RSA-2048 simulated';
      }

      setLogs((prev) => ({
        network: [`[${protocol}] Ciphertext: ${encrypted}`, ...prev.network].slice(0, 12),
        recipient: [`Plaintext: ${decrypted}`, ...prev.recipient].slice(0, 12),
        preview: [`Preview: ${encrypted.slice(0, 120)}`, ...prev.preview].slice(0, 12),
      }));
      setIncoming((prev) => [`${protocol}: ${encrypted}`, ...prev].slice(0, 30));
      setMessage('');
      setStatus(`Message processed in ${mode} mode`);
    } catch (error) {
      setStatus(error.message);
    }
  };

  const decryptMessage = () => {
    const input = decryptInput.trim();
    if (!input) return;
    try {
      const output =
        mode === 'Symmetric'
          ? caesar(input, Number.parseInt(keyInput, 10), true)
          : fromBase64(input);
      setDecryptOutput(output);
      setStatus('Ciphertext decrypted');
    } catch {
      setStatus('Could not decrypt payload');
    }
  };

  const exportText = (filename, content) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const exportTranscript = () => {
    const transcript = [
      '=== SecureBot / Network Intercept ===',
      ...logs.network,
      '',
      '=== Recipient View ===',
      ...logs.recipient,
      '',
      '=== Preview ===',
      ...logs.preview,
    ].join('\n');
    exportText('transcript.txt', transcript);
    setStatus('Transcript exported');
  };

  const exportSession = () => {
    const content = `Mode: ${mode}\nKey: ${computedKey}\n\nIncoming:\n${incoming.join('\n')}`;
    exportText('session.txt', content);
    setStatus('Session exported');
  };

  const importKey = () => {
    const value = window.prompt('Enter a key value:', keyInput);
    if (value !== null && mode !== 'Asymmetric') {
      setKeyInput(value.trim() || '3');
      setStatus('Key imported');
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <TopBar tabs={tabs} activePath={activePath} onNavigate={navigate} onNewSession={newSession} />

      <main className="grid grid-cols-1 gap-3 p-4 xl:grid-cols-[1fr_300px]">
        <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
          <div className="mb-4 flex items-center gap-2">
            <h1 className="text-xl font-bold text-slate-800">{activeLabel}</h1>
            <div className="ml-auto flex gap-2">
              <button onClick={clearHistory} className="rounded-xl border border-slate-200 px-3 py-1 text-xs font-medium hover:bg-slate-100">Clear History</button>
              <button onClick={exportTranscript} className="rounded-xl bg-brand px-3 py-1 text-xs font-semibold text-white hover:bg-sky-500">Export Transcript</button>
            </div>
          </div>

          <Routes>
            <Route path="/" element={<ChatWorkspaceView logs={logs} />} />
            <Route
              path="/decryption"
              element={
                <DecryptionView
                  decryptInput={decryptInput}
                  setDecryptInput={setDecryptInput}
                  decryptOutput={decryptOutput}
                  onDecrypt={decryptMessage}
                />
              }
            />
            <Route
              path="/receive"
              element={
                <ReceivePaneView
                  incoming={incoming}
                  onSelectIncoming={(item) => {
                    const payload = item.split(': ').slice(1).join(': ');
                    setDecryptInput(payload);
                    navigate('/decryption');
                    setStatus('Loaded payload to Decryption Panel');
                  }}
                />
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>

          {activePath === '/' && (
            <ComposerBar
              mode={mode}
              setMode={setMode}
              message={message}
              setMessage={setMessage}
              onSend={processMessage}
              onClear={() => setMessage('')}
            />
          )}
          <p className="mt-3 text-xs text-slate-500">{status}</p>
        </section>

        <SessionPanel
          mode={mode}
          computedKey={computedKey}
          logs={logs}
          incoming={incoming}
          onKeyChange={setKeyInput}
          onImportKey={importKey}
          onExportSession={exportSession}
        />
      </main>
    </div>
  );
}

export default App;
