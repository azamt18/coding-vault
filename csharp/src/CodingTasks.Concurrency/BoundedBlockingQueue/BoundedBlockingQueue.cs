using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;

namespace CodingTasks.Concurrency.BoundedBlockingQueue;

/// <summary>
/// Thread-safe bounded blocking queue using SemaphoreSlim.
/// Supports high-throughput producer-consumer scenarios.
/// </summary>
public class BoundedBlockingQueue<T>
{
    private readonly ConcurrentQueue<T> _queue = new();
    private readonly SemaphoreSlim _producers;
    private readonly SemaphoreSlim _consumers;

    public int Count => _queue.Count;

    public BoundedBlockingQueue(int capacity)
    {
        if (capacity <= 0)
            throw new System.ArgumentException("Capacity must be positive.", nameof(capacity));

        _producers = new SemaphoreSlim(capacity, capacity);
        _consumers = new SemaphoreSlim(0, capacity);
    }

    public async Task EnqueueAsync(T item, CancellationToken cancellationToken = default)
    {
        await _producers.WaitAsync(cancellationToken);
        _queue.Enqueue(item);
        _consumers.Release();
    }

    public async Task<T> DequeueAsync(CancellationToken cancellationToken = default)
    {
        await _consumers.WaitAsync(cancellationToken);
        if (_queue.TryDequeue(out var item))
        {
            _producers.Release();
            return item;
        }

        throw new System.InvalidOperationException("Queue was empty despite consumer permit.");
    }
}
