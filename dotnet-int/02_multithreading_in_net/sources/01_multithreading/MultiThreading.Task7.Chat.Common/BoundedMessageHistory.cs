namespace MultiThreading.Task7.Chat.Common;

/// <summary>
/// Thread-safe in-memory circular/bounded storage for the last N chat messages.
/// </summary>
public sealed class BoundedMessageHistory
{
    private readonly int _capacity;
    private readonly Queue<ChatMessage> _messages;
    private readonly object _syncRoot = new();

    public BoundedMessageHistory(int capacity = 20)
    {
        if (capacity <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(capacity), "Capacity must be positive.");
        }

        _capacity = capacity;
        _messages = new Queue<ChatMessage>(capacity);
    }

    public int Capacity => _capacity;

    public void Add(ChatMessage message)
    {
        ArgumentNullException.ThrowIfNull(message);

        lock (_syncRoot)
        {
            _messages.Enqueue(message);
            if (_messages.Count > _capacity)
            {
                _messages.Dequeue();
            }
        }
    }

    public IReadOnlyList<ChatMessage> GetRecentMessages()
    {
        lock (_syncRoot)
        {
            return _messages.ToArray();
        }
    }
}
