using System.Net.Sockets;
using System.Threading.Channels;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Server;

public sealed class AsyncClientSession : IAsyncDisposable
{
    private readonly Channel<ChatMessage> _outbox;
    private readonly CancellationTokenSource _cts = new();
    private Task? _outboxProcessingTask;
    private bool _isDisposed;

    public AsyncClientSession(Guid id, string clientName, TcpClient tcpClient)
    {
        Id = id;
        ClientName = clientName;
        TcpClient = tcpClient;
        Stream = tcpClient.GetStream();

        _outbox = Channel.CreateUnbounded<ChatMessage>(new UnboundedChannelOptions
        {
            SingleReader = true,
            SingleWriter = false
        });
    }

    public Guid Id { get; }
    public string ClientName { get; }
    public TcpClient TcpClient { get; }
    public NetworkStream Stream { get; }
    public bool IsConnected => TcpClient.Connected && !_isDisposed;

    public void StartOutboxProcessing()
    {
        _outboxProcessingTask = ProcessOutboxAsync(_cts.Token);
    }

    public bool EnqueueMessage(ChatMessage message)
    {
        if (_isDisposed)
        {
            return false;
        }

        return _outbox.Writer.TryWrite(message);
    }

    private async Task ProcessOutboxAsync(CancellationToken cancellationToken)
    {
        try
        {
            await foreach (ChatMessage message in _outbox.Reader.ReadAllAsync(cancellationToken).ConfigureAwait(false))
            {
                await MessageFraming.WriteMessageAsync(Stream, message, cancellationToken).ConfigureAwait(false);
            }
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            // Clean cancellation during shutdown or disconnection
        }
        catch (IOException)
        {
            // Network connection dropped or socket was closed
        }
        catch (SocketException)
        {
            // Socket reset by remote peer
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[AsyncSession] Outbox processing error for '{ClientName}': {ex.Message}");
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_isDisposed)
        {
            return;
        }

        _isDisposed = true;
        _outbox.Writer.TryComplete();
        _cts.Cancel();

        if (_outboxProcessingTask != null)
        {
            try
            {
                await _outboxProcessingTask.ConfigureAwait(false);
            }
            catch
            {
                // Ignore task cancellation on cleanup
            }
        }

        Stream.Dispose();
        TcpClient.Dispose();
        _cts.Dispose();
    }
}
