export const toBase64 = (value) => window.btoa(unescape(encodeURIComponent(value)));

export const fromBase64 = (value) => decodeURIComponent(escape(window.atob(value)));

export const caesar = (text, shift, decrypt = false) => {
  const activeShift = decrypt ? -shift : shift;
  return text
    .split('')
    .map((char) => {
      if (!/[a-z]/i.test(char)) return char;
      const start = char >= 'a' && char <= 'z' ? 97 : 65;
      const code = ((char.charCodeAt(0) - start + activeShift) % 26 + 26) % 26;
      return String.fromCharCode(start + code);
    })
    .join('');
};
