import {
  appendDecimal,
  appendDigit,
  backspace,
  compute,
  formatDisplay,
  parseDisplay,
} from './calculator.js';

const displayEl = document.getElementById('display');
const expressionEl = document.getElementById('expression');
const keypadEl = document.getElementById('keypad');

/** @type {import('./calculator.js').Operator | null} */
let pendingOperator = null;
let accumulator = null;
let waitingForOperand = false;
let currentInput = '0';

const symbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };

function updateDisplay() {
  displayEl.textContent = currentInput;
  expressionEl.textContent =
    accumulator !== null && pendingOperator
      ? `${formatDisplay(accumulator)} ${symbols[pendingOperator]}`
      : '';
}

function resetAll() {
  pendingOperator = null;
  accumulator = null;
  waitingForOperand = false;
  currentInput = '0';
  updateDisplay();
}

function setError() {
  currentInput = 'Error';
  pendingOperator = null;
  accumulator = null;
  waitingForOperand = true;
  updateDisplay();
}

function inputDigit(digit) {
  if (currentInput === 'Error') currentInput = '0';
  if (waitingForOperand) {
    currentInput = digit;
    waitingForOperand = false;
  } else {
    currentInput = appendDigit(currentInput, digit);
  }
  updateDisplay();
}

function inputDecimal() {
  if (currentInput === 'Error') currentInput = '0';
  if (waitingForOperand) {
    currentInput = '0';
    waitingForOperand = false;
  }
  currentInput = appendDecimal(currentInput);
  updateDisplay();
}

function inputBackspace() {
  if (waitingForOperand) return;
  currentInput = backspace(currentInput);
  updateDisplay();
}

function resolvePending() {
  if (accumulator === null || !pendingOperator) return true;
  const result = compute(accumulator, parseDisplay(currentInput), pendingOperator);
  if (result === null) {
    setError();
    return false;
  }
  accumulator = result;
  currentInput = formatDisplay(result);
  return true;
}

function inputOperator(operator) {
  if (currentInput === 'Error') return;

  const currentValue = parseDisplay(currentInput);

  if (accumulator === null) {
    accumulator = currentValue;
  } else if (!waitingForOperand) {
    if (!resolvePending()) return;
  }

  pendingOperator = operator;
  waitingForOperand = true;
  updateDisplay();
}

function inputEquals() {
  if (currentInput === 'Error' || !pendingOperator || accumulator === null) return;

  const right = parseDisplay(currentInput);
  const result = compute(accumulator, right, pendingOperator);

  if (result === null) {
    setError();
    return;
  }

  expressionEl.textContent = `${formatDisplay(accumulator)} ${symbols[pendingOperator]} ${formatDisplay(right)} =`;
  currentInput = formatDisplay(result);
  pendingOperator = null;
  accumulator = null;
  waitingForOperand = true;
  displayEl.textContent = currentInput;
}

function handleAction(action) {
  const ops = { add: '+', subtract: '-', multiply: '*', divide: '/' };

  switch (action) {
    case 'clear':
      resetAll();
      break;
    case 'backspace':
      inputBackspace();
      break;
    case 'decimal':
      inputDecimal();
      break;
    case 'equals':
      inputEquals();
      break;
    default:
      if (ops[action]) inputOperator(ops[action]);
      else if (/^digit-\d$/.test(action)) inputDigit(action.replace('digit-', ''));
  }
}

keypadEl.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]');
  if (button) handleAction(button.dataset.action);
});

document.addEventListener('keydown', (event) => {
  const { key } = event;
  if (/^\d$/.test(key)) {
    event.preventDefault();
    inputDigit(key);
    return;
  }
  const map = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
    Enter: 'equals',
    '=': 'equals',
    Backspace: 'backspace',
    Escape: 'clear',
    ',': 'decimal',
    '.': 'decimal',
  };
  if (map[key]) {
    event.preventDefault();
    handleAction(map[key]);
  }
});

updateDisplay();
