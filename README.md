# ⚡ Coding Vault: Algorithms, Low-Level Design & Concurrency in C# and Python

[![.NET CI](https://github.com/azamt18/coding-vault/actions/workflows/csharp-ci.yml/badge.svg)](https://github.com/azamt18/coding-vault/actions/workflows/csharp-ci.yml)
[![Python CI](https://github.com/azamt18/coding-vault/actions/workflows/python-ci.yml/badge.svg)](https://github.com/azamt18/coding-vault/actions/workflows/python-ci.yml)
[![LeetCode Profile](https://img.shields.io/badge/LeetCode-azamt18-FFA116?style=flat&logo=leetcode&logoColor=black)](https://leetcode.com/u/azamt18/)

A unified, high-performance polyglot monorepo dedicated to **Senior Software Engineering Interview Preparation**, **Algorithmic Problem Solving**, **Low-Level / Object-Oriented Design (LLD)**, and **Multithreading / Concurrency** in **C# (.NET 10)** and **Python 3**.

---

## 📊 Live LeetCode Stats

<p align="center">
  <a href="https://leetcode.com/u/azamt18/">
    <img src="https://leetcard.jacoblin.cool/azamt18?theme=dark&font=Ubuntu&ext=activity" alt="LeetCode Stats - azamt18" />
  </a>
</p>

---

## 🏛️ Monorepo Architecture

```text
coding-vault/
├── .github/
│   └── workflows/
│       ├── csharp-ci.yml                   # Automated dotnet test CI runner
│       └── python-ci.yml                   # Automated pytest CI runner
│
├── csharp/                                 # C# .NET 10 Solution
│   ├── CodingTasks.sln
│   ├── src/
│   │   ├── CodingTasks.DSA/                # Algorithmic Problems by Pattern
│   │   │   ├── ArraysAndHashing/
│   │   │   ├── TwoPointers/
│   │   │   ├── SlidingWindow/
│   │   │   ├── BinarySearch/
│   │   │   ├── TreesAndGraphs/
│   │   │   └── DynamicProgramming/
│   │   │
│   │   ├── CodingTasks.Design/             # Low-Level / Object-Oriented Design (LLD)
│   │   │   ├── LruCache/                   # O(1) Double LinkedList + HashMap
│   │   │   ├── RateLimiter/                # Token Bucket, Sliding Window Counter
│   │   │   ├── ParkingSystem/
│   │   │   └── FileSystem/
│   │   │
│   │   ├── CodingTasks.Concurrency/        # Multithreading & Thread-Safe Primitives
│   │   │   ├── BoundedBlockingQueue/       # Producer-Consumer with SemaphoreSlim
│   │   │   ├── ReadWriteLock/
│   │   │   └── ThreadSafeCache/
│   │   │
│   │   ├── CodingTasks.DataStructures/     # Custom Core Data Structures
│   │   │   └── Tree/                       # BinaryTreeTraversal (Recursive & Iterative)
│   │   │
│   │   └── CodingTasks.Utilities/          # Modular Reusable Engineering Utilities
│   │       ├── Hashing/                    # SHA-256 / BouncyCastle Hashing
│   │       ├── AddressToPost/              # Levenshtein Distance & Fuzzy Matcher
│   │       ├── JsonComparer/               # Status & Delta Comparer
│   │       ├── Parsing/                    # Csv & Data Readers
│   │       └── Renamer/                    # High-throughput String Aggregators
│   │
│   └── tests/
│       └── CodingTasks.Tests/              # NUnit 4.x + FluentAssertions 8.x
│
├── python/                                 # Python 3 Algorithmic Workspace
│   ├── dsa/                                # Curated LeetCode & DSA Problem Solutions
│   └── tests/                              # pytest Suite
│
└── ROADMAP.md                              # Detailed Interview Milestones & Study Plan
```

---

## 🎯 Interview Mastery Roadmap

| Area | Key Topics Covered | Target |
| :--- | :--- | :--- |
| **Data Structures & Algorithms** | Arrays, Hashing, Two Pointers, Sliding Window, Trees, Graphs, DP | Blind 75 / NeetCode 150 |
| **Low-Level Design (LLD / OOD)** | LRU Cache, Rate Limiter, In-Memory DB, SOLID & Design Patterns | Senior SDE Standards |
| **Concurrency & Multithreading** | `SemaphoreSlim`, `ConcurrentQueue`, `Channel<T>`, `Interlocked`, Locks | Production & High Throughput |
| **Testing & Verification** | NUnit Unit Tests, Property-based Tests, FluentAssertions | 100% Core Logic Coverage |

---

## 🚀 Quick Start

### C# (.NET 10)
```bash
# Build the entire solution
dotnet build csharp/CodingTasks.sln

# Run all NUnit tests
dotnet test csharp/CodingTasks.sln
```

### Python 3
```bash
# Install dependencies
pip install -r python/requirements.txt

# Run pytest
pytest python/tests
```
