<div align="center">

# ⚡ Coding Vault
### High-Performance Algorithms, Low-Level Design (LLD) & Concurrency in C# and Python

[![.NET 10](https://img.shields.io/badge/.NET-10.0-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![C#](https://img.shields.io/badge/C%23-13%2B-239120?style=for-the-badge&logo=csharp&logoColor=white)](https://docs.microsoft.com/en-us/dotnet/csharp/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NUnit Tested](https://img.shields.io/badge/NUnit-Tested-25A162?style=for-the-badge&logo=nunit&logoColor=white)](https://nunit.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Passing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![LeetCode Profile](https://img.shields.io/badge/LeetCode-600%2B%20Solved-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/u/azamt18/)

</div>

---

A unified, high-performance polyglot repository dedicated to **Senior Software Engineering Interview Preparation**, **Algorithmic Problem Solving**, **Low-Level Object-Oriented Design (LLD)**, and **Multithreading / Concurrency** in **C# (.NET 10)** and **Python 3.12**.

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
├── dotnet-int/                             # .NET Intermediate Mentoring Program Modules
│   ├── 01_help_module/
│   ├── 02_multithreading_in_net/           # Multithreading, ThreadPool, Mutex, Monitor
│   ├── 03_async_programming/              # Async/Await, Task Parallel Library (TPL)
│   ├── 04_message_queues/                  # Producer-Consumer & Queue patterns
│   ├── 05_analyzing_and_profiling_tools/   # Memory/CPU Profiling & Performance
│   ├── 06_linq_iqueryable/                 # Custom LINQ providers & IQueryable
│   ├── 07_expressions/                     # Expression Trees & Dynamic Queries
│   ├── 08_rest_architecture/              # RESTful API Design & Best Practices
│   ├── 09_hosting_and_deployment/          # Kestrel, Hosting Models, & Environments
│   └── 10-14_gof_design_patterns/          # Creational, Structural, Behavioral GoF Patterns
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
