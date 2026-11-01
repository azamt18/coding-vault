import { describe, expect, it } from 'vitest';
import { isWordBoundary, planConversion } from './typing';

describe('isWordBoundary', () => {
  it.each([' ', '\n', ',', '!', '?', ';', ')', '"', '»', '…'])(
    'treats %j as the end of a word',
    (char) => {
      expect(isWordBoundary(char)).toBe(true);
    },
  );

  // A dot or colon may be part of a domain or link (shahar.uz, https://), which
  // can't be told apart from a sentence end until the whole token is typed.
  it.each(['a', 'h', "'", 'ʻ', '’', '-', '1', '.', ':', '/', '@'])('keeps typing the word after %j', (char) => {
    expect(isWordBoundary(char)).toBe(false);
  });
});

describe('planConversion', () => {
  it('converts the word right before the caret', () => {
    expect(planConversion('Men shahar', 10)).toEqual({
      start: 4,
      end: 10,
      original: 'shahar',
      replacement: 'şahar',
    });
  });

  it('only looks at text before the caret', () => {
    expect(planConversion('choy | qalesan', 4)).toEqual({
      start: 0,
      end: 4,
      original: 'choy',
      replacement: 'çoy',
    });
  });

  it('returns null when nothing would change', () => {
    expect(planConversion('Men kitob', 9)).toBeNull();
    expect(planConversion('my shop', 7)).toBeNull();
  });

  it('returns null when the caret is right after whitespace', () => {
    expect(planConversion('shahar ', 7)).toBeNull();
    expect(planConversion('', 0)).toBeNull();
  });

  it('passes the skip list through', () => {
    expect(planConversion('Shohruh', 7, { skipWords: new Set(['shohruh']) })).toBeNull();
  });
});
