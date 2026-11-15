import { describe, expect, it, vi } from "vitest";
import bank from "../data/anxious-generation.json";
import type { QuestionBank } from "../types";
import {
  ANXIOUS_GENERATION_TITLES,
  OFFLINE_NOTE,
  buildChapters,
  fetchBookByTitle,
  loadBook,
} from "./openLibrary";

const questionBank = bank as unknown as QuestionBank;
const chapters = buildChapters(ANXIOUS_GENERATION_TITLES);

describe("question bank", () => {
  it("has a local chapter and at least 2 questions for every chapter number", () => {
    const numbers = Object.keys(questionBank).map(Number);
    expect(numbers.length).toBeGreaterThan(0);
    for (const n of numbers) {
      expect(chapters.some((c) => c.number === n)).toBe(true);
      expect(questionBank[n].length).toBeGreaterThanOrEqual(2);
    }
  });

  it("covers every local chapter", () => {
    for (const c of chapters) expect(questionBank[c.number]).toBeDefined();
  });

  it("has unique ids and consistent chapter fields", () => {
    const all = Object.entries(questionBank).flatMap(([k, qs]) =>
      qs.map((q) => ({ k: Number(k), q })),
    );
    const ids = all.map(({ q }) => q.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const { k, q } of all) {
      expect(q.chapter).toBe(k);
      const prefix = k === 0 ? "intro" : `ch${k}`;
      expect(q.id.startsWith(`${prefix}-q`)).toBe(true);
    }
  });
});

const okFetch = (docs: unknown[]) =>
  vi.fn(async () => ({ ok: true, json: async () => ({ docs }) }) as Response);

describe("open library loading", () => {
  it("rejects results whose author is not haidt", async () => {
    const f = okFetch([{ title: "summary", author_name: ["someone else"] }]);
    await expect(fetchBookByTitle("The Anxious Generation", f)).rejects.toThrow();
  });

  it("accepts a haidt result", async () => {
    const f = okFetch([
      { title: "summary", author_name: ["x"] },
      { title: "The anxious generation", author_name: ["Jonathan Haidt"] },
    ]);
    const book = await fetchBookByTitle("The Anxious Generation", f);
    expect(book.author).toBe("Jonathan Haidt");
  });

  it("falls back to the local book on error", async () => {
    const f = vi.fn(async () => {
      throw new Error("network");
    }) as unknown as typeof fetch;
    const { book, offline } = await loadBook("The Anxious Generation", f);
    expect(offline).toBe(true);
    expect(book.chapters.length).toBe(ANXIOUS_GENERATION_TITLES.length);
    expect(OFFLINE_NOTE).toMatch(/offline/);
  });

  it("falls back on timeout", async () => {
    const f = ((_u: string, init?: RequestInit) =>
      new Promise((_r, rej) => {
        init?.signal?.addEventListener("abort", () => rej(new Error("aborted")));
      })) as unknown as typeof fetch;
    const { offline } = await loadBook("The Anxious Generation", f, 20);
    expect(offline).toBe(true);
  });
});
