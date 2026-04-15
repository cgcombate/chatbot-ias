export const tabs = [
  { label: 'Chat Workspace', path: '/' },
  { label: 'Decryption Panel', path: '/decryption' },
  { label: 'Message Receive Pane', path: '/receive' },
];

export const tabLabelByPath = Object.fromEntries(tabs.map((tab) => [tab.path, tab.label]));
