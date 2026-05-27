/** @typedef {'+' | '-' | '*' | '/'} Operator */

export const MAX_DISPLAY_LENGTH = 16;

/**
 * @param {number} a
 * @param {number} b
 * @param {Operator} operator
 * @returns {number | null}
 */
export function compute(a, b, operator) {
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;

  switch (operator) {
    case '+':
      return a + b;
    case '-':
      return a - b;
    case '*':
      return a * b;
    case '/':
      if (b === 0) return null;
      return a / b;
    default:
      return null;
  }
}

/**
 * @param {number} value
 * @param {number} [maxLength]
 */
export function formatDisplay(value, maxLength = MAX_DISPLAY_LENGTH) {
  if (!Number.isFinite(value)) return 'Error';

  const rounded = Math.round(value * 1e10) / 1e10;
  let text = String(rounded);

  if (text.length > maxLength) {
    text = rounded.toExponential(maxLength - 5);
  }
  if (text.length > maxLength) {
    text = text.slice(0, maxLength);
  }

  return text;
}

/**
 * @param {string} current
 * @param {string} digit
 */
export function appendDigit(current, digit) {
  if (!/^\d$/.test(digit)) return current;
  if (current === '0' && digit !== '.') return digit;
  if (current.length >= MAX_DISPLAY_LENGTH) return current;
  return current + digit;
}

/**
 * @param {string} current
 */
export function appendDecimal(current) {
  if (current.includes('.')) return current;
  if (current.length >= MAX_DISPLAY_LENGTH) return current;
  return `${current}.`;
}

/**
 * @param {string} current
 */
export function backspace(current) {
  if (!current || current === 'Error') return '0';
  const next = current.slice(0, -1);
  return next === '' || next === '-' ? '0' : next;
}

/**
 * @param {string} text
 */
export function parseDisplay(text) {
  const value = Number.parseFloat(text);
  return Number.isFinite(value) ? value : 0;
}
