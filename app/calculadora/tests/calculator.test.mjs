import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  appendDecimal,
  appendDigit,
  backspace,
  compute,
  formatDisplay,
  parseDisplay,
} from '../js/calculator.js';

describe('compute', () => {
  it('suma, resta, multiplica y divide', () => {
    assert.equal(compute(2, 3, '+'), 5);
    assert.equal(compute(10, 4, '-'), 6);
    assert.equal(compute(3, 4, '*'), 12);
    assert.equal(compute(15, 3, '/'), 5);
  });

  it('devuelve null en división por cero', () => {
    assert.equal(compute(1, 0, '/'), null);
    assert.equal(compute(0, 0, '/'), null);
  });

  it('rechaza operandos no finitos', () => {
    assert.equal(compute(NaN, 1, '+'), null);
    assert.equal(compute(1, Infinity, '+'), null);
  });
});

describe('formatDisplay', () => {
  it('formatea números normales', () => {
    assert.equal(formatDisplay(42), '42');
    assert.equal(formatDisplay(0.1 + 0.2), '0.3');
  });

  it('muestra Error para no finitos', () => {
    assert.equal(formatDisplay(NaN), 'Error');
    assert.equal(formatDisplay(Infinity), 'Error');
  });
});

describe('appendDigit', () => {
  it('reemplaza cero inicial', () => {
    assert.equal(appendDigit('0', '5'), '5');
  });

  it('concatena dígitos', () => {
    assert.equal(appendDigit('12', '3'), '123');
  });
});

describe('appendDecimal', () => {
  it('añade punto una sola vez', () => {
    assert.equal(appendDecimal('12'), '12.');
    assert.equal(appendDecimal('12.'), '12.');
  });
});

describe('backspace', () => {
  it('borra último carácter', () => {
    assert.equal(backspace('123'), '12');
    assert.equal(backspace('1'), '0');
  });
});

describe('parseDisplay', () => {
  it('parsea números válidos', () => {
    assert.equal(parseDisplay('3.14'), 3.14);
    assert.equal(parseDisplay('abc'), 0);
  });
});
