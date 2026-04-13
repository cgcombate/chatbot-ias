export const tabs = [
  { label: 'Chat Workspace', path: '/' },
  { label: 'Encryption Mode Selector', path: '/encryption' },
  { label: 'Decryption Panel', path: '/decryption' },
  { label: 'Message Receive Pane', path: '/receive' },
];

export const tabLabelByPath = Object.fromEntries(tabs.map((tab) => [tab.path, tab.label]));
