using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Server;

public sealed class AsyncChatServer : IAsyncDisposable
{
    private readonly int _port;
    private readonly BoundedMessageHistory _history;
    private readonly ConcurrentDictionary<Guid, AsyncClientSession> _clients = new();
    private readonly CancellationTokenSource _cts = new();
    private TcpListener? _listener;
    private Task? _listenerTask;
    private volatile bool _isRunning;

    public AsyncChatServer(int port = 5050, int historyCapacity = 20)
    {
        _port = port;
        _history = new BoundedMessageHistory(historyCapacity);
    }

    public int Port => _port;
    public bool IsRunning => _isRunning;

    public void Start()
    {
        if (_isRunning)
        {
            return;
        }

        _isRunning = true;
        _listener = new TcpListener(IPAddress.Loopback, _port);
        _listener.Start();

        _listenerTask = ListenLoopAsync(_cts.Token);
        Console.WriteLine($"[AsyncServer] Started on port {_port}. Listening for connections (TPL / Async)...");
    }

    private async Task ListenLoopAsync(CancellationToken cancellationToken)
    {
        while (!cancellationToken.IsCancellationRequested)
        {
            try
            {
                TcpClient tcpClient = await _listener!.AcceptTcpClientAsync(cancellationToken).ConfigureAwait(false);
                Guid clientId = Guid.NewGuid();

                // Fire-and-forget task per client connection
                _ = HandleClientAsync(tcpClient, clientId, cancellationToken);
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
                break;
            }
            catch (SocketException) when (!_isRunning)
            {
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[AsyncServer] Error accepting client: {ex.Message}");
            }
        }
    }

    private async Task HandleClientAsync(TcpClient tcpClient, Guid clientId, CancellationToken serverCancellationToken)
    {
        using var clientCts = CancellationTokenSource.CreateLinkedTokenSource(serverCancellationToken);
        AsyncClientSession? session = null;

        try
        {
            NetworkStream stream = tcpClient.GetStream();

            // 1. Handshake
            ChatMessage? handshake = await MessageFraming.ReadMessageAsync(stream, clientCts.Token).ConfigureAwait(false);
            if (handshake == null || string.IsNullOrWhiteSpace(handshake.SentBy))
            {
                Console.WriteLine($"[AsyncServer] Client {clientId} failed handshake. Closing.");
                tcpClient.Dispose();
                return;
            }

            string clientName = handshake.SentBy;
            session = new AsyncClientSession(clientId, clientName, tcpClient);
            session.StartOutboxProcessing();

            _clients[clientId] = session;
            Console.WriteLine($"[AsyncServer] '{clientName}' connected (ThreadPool Thread: {Thread.CurrentThread.ManagedThreadId}, Total clients: {_clients.Count}).");

            // 2. Replay history
            IReadOnlyList<ChatMessage> recent = _history.GetRecentMessages();
            foreach (ChatMessage historicalMsg in recent)
            {
                session.EnqueueMessage(historicalMsg);
            }

            // 3. Broadcast Join
            ChatMessage joinNotification = ChatMessage.Join(clientName);
            _history.Add(joinNotification);
            Broadcast(joinNotification, excludeSessionId: session.Id);

            // 4. Message receive loop
            while (!clientCts.IsCancellationRequested && session.IsConnected)
            {
                ChatMessage? incoming = await MessageFraming.ReadMessageAsync(stream, clientCts.Token).ConfigureAwait(false);
                if (incoming == null || incoming.Type == ChatMessageType.Disconnect)
                {
                    break;
                }

                Console.WriteLine($"[AsyncServer] Received from '{clientName}': {incoming.Text}");
                _history.Add(incoming);
                Broadcast(incoming, excludeSessionId: session.Id);
            }
        }
        catch (OperationCanceledException)
        {
            // Expected on client or server cancellation
        }
        catch (IOException)
        {
            // Socket disconnected
        }
        catch (SocketException)
        {
            // Socket reset
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[AsyncServer] Unexpected error with client {clientId}: {ex.Message}");
        }
        finally
        {
            if (session != null)
            {
                await UnregisterAndDisconnectClientAsync(session).ConfigureAwait(false);
            }
            else
            {
                tcpClient.Dispose();
            }
        }
    }

    private async Task UnregisterAndDisconnectClientAsync(AsyncClientSession session)
    {
        if (_clients.TryRemove(session.Id, out _))
        {
            Console.WriteLine($"[AsyncServer] '{session.ClientName}' disconnected (Clients remaining: {_clients.Count}).");

            ChatMessage leaveNotification = ChatMessage.Disconnect(session.ClientName);
            _history.Add(leaveNotification);
            Broadcast(leaveNotification, excludeSessionId: session.Id);
        }

        await session.DisposeAsync().ConfigureAwait(false);
    }

    public void Broadcast(ChatMessage message, Guid? excludeSessionId = null)
    {
        foreach (KeyValuePair<Guid, AsyncClientSession> kvp in _clients)
        {
            if (kvp.Key != excludeSessionId && kvp.Value.IsConnected)
            {
                kvp.Value.EnqueueMessage(message);
            }
        }
    }

    public int GetClientCount() => _clients.Count;

    public async Task StopAsync()
    {
        if (!_isRunning)
        {
            return;
        }

        _isRunning = false;
        Console.WriteLine("[AsyncServer] Stopping server and notifying clients...");

        // Notify clients
        ChatMessage shutdownMsg = ChatMessage.System("Server is shutting down. Goodbye!");
        Broadcast(shutdownMsg);

        // Cancel token & stop listener
        _cts.Cancel();
        try
        {
            _listener?.Stop();
        }
        catch
        {
            // Ignore listener stop errors
        }

        if (_listenerTask != null)
        {
            try
            {
                await _listenerTask.ConfigureAwait(false);
            }
            catch
            {
                // Ignore cancellation
            }
        }

        // Dispose all clients concurrently
        AsyncClientSession[] activeSessions = _clients.Values.ToArray();
        _clients.Clear();

        await Task.WhenAll(activeSessions.Select(s => s.DisposeAsync().AsTask())).ConfigureAwait(false);

        _cts.Dispose();
        Console.WriteLine("[AsyncServer] Server stopped successfully.");
    }

    public async ValueTask DisposeAsync()
    {
        await StopAsync().ConfigureAwait(false);
    }
}
