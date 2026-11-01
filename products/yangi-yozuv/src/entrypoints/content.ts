import { isWordBoundary, planConversion } from '@/core/typing';
import { disabledSitesItem, enabledItem, skipWordsItem } from '@/utils/settings';
import { DEFAULT_SITES, EXCLUDED_SITES } from '@/utils/sites';

type Editable = HTMLInputElement | HTMLTextAreaElement | HTMLElement;

/** Text before the caret, and a way to select part of it for replacing. */
interface CaretContext {
  text: string;
  caret: number;
  select(start: number, end: number): void;
}

// Input types where people type words; email, url and password stay untouched.
const TEXT_INPUT_TYPES = new Set(['text', 'search', '']);

export default defineContentScript({
  matches: DEFAULT_SITES,
  excludeMatches: EXCLUDED_SITES,
  allFrames: true,
  runAt: 'document_idle',

  async main() {
    // The background worker can inject this script into a tab that already
    // has it (after the user switches a site on), so guard against doubling.
    const flagged = window as unknown as { __yangiYozuv?: boolean };
    if (flagged.__yangiYozuv) return;
    flagged.__yangiYozuv = true;

    let enabled = await enabledItem.getValue();
    let siteDisabled = (await disabledSitesItem.getValue()).includes(location.hostname);
    let skipWords = new Set(await skipWordsItem.getValue());
    enabledItem.watch((value) => (enabled = value));
    disabledSitesItem.watch((value) => (siteDisabled = value.includes(location.hostname)));
    skipWordsItem.watch((value) => (skipWords = new Set(value)));

    // What the last conversion inserted, so one Backspace can undo it.
    let lastConversion: { target: Editable; original: string; inserted: string } | null = null;

    document.addEventListener(
      'beforeinput',
      (event) => {
        if (!enabled || siteDisabled) return;
        if (event.isComposing || event.inputType !== 'insertText') return;
        if (!event.data || !isWordBoundary(event.data)) return;

        const target = editableTarget(event.target);
        const context = target && caretContext(target);
        if (!target || !context) return;

        const plan = planConversion(context.text, context.caret, { skipWords });
        if (!plan) return;

        // Replace the word and type the boundary in one edit, so the page's
        // own editor (Telegram, Gmail) sees a normal insertion.
        event.preventDefault();
        context.select(plan.start, plan.end);
        const inserted = plan.replacement + event.data;
        document.execCommand('insertText', false, inserted);
        lastConversion = { target, original: plan.original + event.data, inserted };
      },
      true,
    );

    // Enter types no character, so beforeinput above never sees it. Convert
    // the last word before the page acts on Enter, because in chat apps Enter
    // sends the message. Listening on document in the capture phase runs
    // before the app's own handlers on the editor.
    document.addEventListener(
      'keydown',
      (event) => {
        if (!enabled || siteDisabled) return;
        if (event.key !== 'Enter' || event.isComposing) return;

        const target = editableTarget(event.target);
        const context = target && caretContext(target);
        if (!target || !context) return;

        const plan = planConversion(context.text, context.caret, { skipWords });
        if (!plan) return;

        context.select(plan.start, plan.end);
        document.execCommand('insertText', false, plan.replacement);
        lastConversion = null;
      },
      true,
    );

    document.addEventListener(
      'keydown',
      (event) => {
        if (!lastConversion) return;
        const { target, original, inserted } = lastConversion;
        if (event.key !== 'Backspace' || event.target !== target) {
          if (!['Shift', 'Control', 'Alt', 'Meta'].includes(event.key)) lastConversion = null;
          return;
        }
        lastConversion = null;

        const context = caretContext(target);
        if (!context) return;
        const start = context.caret - inserted.length;
        if (start < 0 || context.text.slice(start, context.caret) !== inserted) return;

        event.preventDefault();
        context.select(start, context.caret);
        document.execCommand('insertText', false, original);
      },
      true,
    );

    document.addEventListener('mousedown', () => (lastConversion = null), true);
  },
});

function editableTarget(node: EventTarget | null): Editable | null {
  if (node instanceof HTMLInputElement) return TEXT_INPUT_TYPES.has(node.type) ? node : null;
  if (node instanceof HTMLTextAreaElement) return node;
  if (node instanceof HTMLElement && node.isContentEditable) return node;
  return null;
}

function caretContext(target: Editable): CaretContext | null {
  if (target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement) {
    const caret = target.selectionStart;
    if (caret === null || caret !== target.selectionEnd) return null;
    return {
      text: target.value,
      caret,
      select: (start, end) => target.setSelectionRange(start, end),
    };
  }

  // Rich editors: only handle a collapsed caret inside a text node. A word
  // split across formatting (half bold) is left alone.
  const selection = window.getSelection();
  const node = selection?.anchorNode;
  if (!selection?.isCollapsed || !(node instanceof Text)) return null;
  return {
    text: node.data,
    caret: selection.anchorOffset,
    select: (start, end) => {
      const range = document.createRange();
      range.setStart(node, start);
      range.setEnd(node, end);
      selection.removeAllRanges();
      selection.addRange(range);
    },
  };
}
