# 🗺️ Interview Preparation & Advanced Topics Roadmap

This roadmap outlines our structured milestone plan for mastering **Algorithms**, **Low-Level System Design (LLD)**, and **C# Advanced Concurrency & Systems Programming**.

---

## 📅 Phase 1: Core Problem Solving & Patterns (Blind 75 & NeetCode 150)

### 1. Arrays & Hashing
- [x] Group Anagrams (`csharp/src/CodingTasks.DSA/ArraysAndHashing/GroupAnagramsSolution.cs`)
- [ ] Two Sum
- [ ] Top K Frequent Elements
- [ ] Product of Array Except Self
- [ ] Longest Consecutive Sequence

### 2. Two Pointers & Sliding Window
- [ ] Valid Palindrome
- [ ] 3Sum
- [ ] Container With Most Water
- [ ] Best Time to Buy and Sell Stock
- [ ] Longest Substring Without Repeating Characters
- [ ] Minimum Window Substring

### 3. Stack & Binary Search
- [ ] Valid Parentheses
- [ ] Min Stack / Monotonic Stack (Daily Temperatures)
- [ ] Binary Search on Rotated Sorted Array
- [ ] Search a 2D Matrix
- [ ] Koko Eating Bananas

### 4. Trees, Heaps & Graphs
- [x] Binary Tree Traversals (Recursive & Iterative)
- [ ] Invert Binary Tree / Maximum Depth
- [ ] Lowest Common Ancestor
- [ ] Task Scheduler / Find Median from Data Stream (Heaps)
- [ ] Number of Islands / Clone Graph / Course Schedule (Graphs & Topo Sort)

### 5. Dynamic Programming & Backtracking
- [ ] Climbing Stairs / Coin Change
- [ ] Longest Increasing Subsequence
- [ ] Word Break
- [ ] Subsets / Combination Sum

---

## 🏗️ Phase 2: Low-Level / Object-Oriented Design (LLD)

- [x] **LRU Cache** (`csharp/src/CodingTasks.Design/LruCache/LruCache.cs`): $O(1)$ Double LinkedList + HashMap
- [ ] **LFU Cache**: Frequency map + doubly linked lists
- [ ] **Rate Limiter**: Token Bucket, Leaky Bucket, Sliding Window Counter
- [ ] **In-Memory Key-Value Store with Transactions**: ACID transactions with rollback support
- [ ] **Parking Lot System**: Object-oriented models with strategy pattern for space allocation
- [ ] **File System / Unix Find Command**: Composite pattern and predicate filters

---

## ⚡ Phase 3: Advanced C# Concurrency & Systems Programming

- [x] **Bounded Blocking Queue** (`csharp/src/CodingTasks.Concurrency/BoundedBlockingQueue/BoundedBlockingQueue.cs`): High-throughput Producer-Consumer with `SemaphoreSlim`
- [ ] **Custom Read-Write Lock**: Fair lock implementation preventing writer starvation
- [ ] **Thread-Safe In-Memory Cache with TTL**: Non-blocking reads with granular locking
- [ ] **High-Throughput Actor / Pipeline using `System.Threading.Channels`**: Backpressure & batching
- [ ] **Zero-Allocation Data Processing**: `Span<T>`, `Memory<T>`, and `ArrayPool<T>` in hot paths

---

## 🧪 Testing & Code Quality Standard

Every single problem, design component, or concurrency primitive implemented must have:
1. **Unit Tests:** NUnit tests verifying standard cases, edge cases (empty, boundary, null).
2. **Behavioral / Stress Tests:** Multithreaded assertions for concurrent components using `Task.WhenAll`.
3. **Automated CI:** Every commit is validated by GitHub Actions (.NET + Python CI).
