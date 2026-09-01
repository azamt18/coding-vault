using System.Collections.Generic;

namespace CodingTasks.Design.LruCache;

/// <summary>
/// LRU (Least Recently Used) Cache implementation using Doubly Linked List and Hash Map.
/// Time Complexity: O(1) for both Get and Put.
/// Space Complexity: O(capacity).
/// </summary>
public class LruCache<TKey, TValue> where TKey : notnull
{
    private class Node
    {
        public TKey Key;
        public TValue Value;
        public Node? Prev;
        public Node? Next;

        public Node(TKey key, TValue value)
        {
            Key = key;
            Value = value;
        }
    }

    private readonly int _capacity;
    private readonly Dictionary<TKey, Node> _map;
    private readonly Node _head;
    private readonly Node _tail;

    public int Count => _map.Count;

    public LruCache(int capacity)
    {
        if (capacity <= 0)
            throw new System.ArgumentException("Capacity must be greater than zero.", nameof(capacity));

        _capacity = capacity;
        _map = new Dictionary<TKey, Node>(capacity);

        _head = new Node(default!, default!);
        _tail = new Node(default!, default!);
        _head.Next = _tail;
        _tail.Prev = _head;
    }

    public bool TryGet(TKey key, out TValue value)
    {
        if (_map.TryGetValue(key, out var node))
        {
            MoveToHead(node);
            value = node.Value;
            return true;
        }

        value = default!;
        return false;
    }

    public void Put(TKey key, TValue value)
    {
        if (_map.TryGetValue(key, out var existingNode))
        {
            existingNode.Value = value;
            MoveToHead(existingNode);
            return;
        }

        if (_map.Count >= _capacity)
        {
            var lru = _tail.Prev!;
            RemoveNode(lru);
            _map.Remove(lru.Key);
        }

        var newNode = new Node(key, value);
        _map[key] = newNode;
        AddToHead(newNode);
    }

    private void AddToHead(Node node)
    {
        node.Next = _head.Next;
        node.Prev = _head;
        _head.Next!.Prev = node;
        _head.Next = node;
    }

    private void RemoveNode(Node node)
    {
        node.Prev!.Next = node.Next;
        node.Next!.Prev = node.Prev;
    }

    private void MoveToHead(Node node)
    {
        RemoveNode(node);
        AddToHead(node);
    }
}
