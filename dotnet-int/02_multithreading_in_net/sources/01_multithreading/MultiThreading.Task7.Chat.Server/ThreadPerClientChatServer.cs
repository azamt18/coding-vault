using System.Net;
using System.Net.Sockets;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Server;

public sealed class ThreadPerClientChatServer : IDisposable
{
    private readonly int _port;
    private readonly BoundedMessageHistory _history;
    private readonly List<ClientSession> _clients = new();
    private readonly object _clientsLock = new();
    private TcpListener? _listener;
    private Thread? _listenerThread;
    private volatile bool _isRunning;

    public ThreadPerClientChatServer(int port = 5050, int historyCapacity = 20)
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

        _listenerThread = new Thread(ListenLoop)
        {
            IsBackground = true,
            Name = "Server-ListenerThread"
        };
        _listenerThread.Start();

        Console.WriteLine($"[Server] Started on port {_port}. Listening for connections...");
    }

    private void ListenLoop()
    {
        while (_isRunning)
        {
            try
            {
                TcpClient tcpClient = _listener!.AcceptTcpClient();
                Guid clientId = Guid.NewGuid();

                Thread clientThread = new Thread(() => HandleClient(tcpClient, clientId))
                {
                    IsBackground = true,
                    Name = $"ClientWorker-{clientId}"
                };
                clientThread.Start();
            }
            catch (SocketException) when (!_isRunning)
            {
                // Normal exit when listener is stopped
                break;
            }
            catch (Exception ex) when (_isRunning)
            {
                Console.WriteLine($"[Server] Error accepting client: {ex.Message}");
            }
        }
    }

    private void HandleClient(TcpClient tcpClient, Guid clientId)
    {
        ClientSession? session = null;
        try
        {
            NetworkStream stream = tcpClient.GetStream();

            // 1. Handshake: Read initial join/handshake message
            ChatMessage? handshake = MessageFraming.ReadMessage(stream);
            if (handshake == null || string.IsNullOrWhiteSpace(handshake.SentBy))
            {
                Console.WriteLine($"[Server] Client {clientId} failed handshake. Closing.");
                tcpClient.Dispose();
                return;
            }

            string clientName = handshake.SentBy;
            session = new ClientSession(clientId, clientName, tcpClient);

            // Register client
            lock (_clientsLock)
            {
                _clients.Add(session);
            }

            Console.WriteLine($"[Server] '{clientName}' connected (Thread: {Thread.CurrentThread.ManagedThreadId}, Clients: {GetClientCount()}).");

            // 2. Replay history to this new client
            IReadOnlyList<ChatMessage> recentHistory = _history.GetRecentMessages();
            foreach (ChatMessage historicalMsg in recentHistory)
            {
                session.Send(historicalMsg);
            }

            // 3. Broadcast Join notification to all other clients
            ChatMessage joinNotification = ChatMessage.Join(clientName);
            _history.Add(joinNotification);
            Broadcast(joinNotification, excludeSessionId: session.Id);

            // 4. Message receive loop
            while (_isRunning && session.IsConnected)
            {
                ChatMessage? incomingMessage = MessageFraming.ReadMessage(stream);
                if (incomingMessage == null || incomingMessage.Type == ChatMessageType.Disconnect)
                {
                    break;
                }

                Console.WriteLine($"[Server] Received from '{clientName}': {incomingMessage.Text}");

                _history.Add(incomingMessage);
                Broadcast(incomingMessage, excludeSessionId: session.Id);
            }
        }
        catch (IOException)
        {
            // Socket was closed or aborted
        }
        catch (SocketException)
        {
            // Connection reset by peer
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[Server] Unexpected error with client {clientId}: {ex.Message}");
        }
        finally
        {
            if (session != null)
            {
                UnregisterAndDisconnectClient(session);
            }
            else
            {
                tcpClient.Dispose();
            }
        }
    }

    private void UnregisterAndDisconnectClient(ClientSession session)
    {
        bool wasRemoved;
        lock (_clientsLock)
        {
            wasRemoved = _clients.Remove(session);
        }

        if (wasRemoved)
        {
            Console.WriteLine($"[Server] '{session.ClientName}' disconnected (Clients remaining: {GetClientCount()}).");

            ChatMessage leaveNotification = ChatMessage.Disconnect(session.ClientName);
            _history.Add(leaveNotification);
            Broadcast(leaveNotification, excludeSessionId: session.Id);
        }

        session.Dispose();
    }

    public void Broadcast(ChatMessage message, Guid? excludeSessionId = null)
    {
        ClientSession[] targets;
        lock (_clientsLock)
        {
            targets = _clients.Where(c => c.Id != excludeSessionId && c.IsConnected).ToArray();
        }

        foreach (ClientSession client in targets)
        {
            try
            {
                client.Send(message);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Server] Failed to send message to '{client.ClientName}': {ex.Message}");
            }
        }
    }

    public int GetClientCount()
    {
        lock (_clientsLock)
        {
            return _clients.Count;
        }
    }

    public void Stop()
    {
        if (!_isRunning)
        {
            return;
        }

        _isRunning = false;
        Console.WriteLine("[Server] Stopping server and notifying clients...");

        // Notify clients about server shutdown
        ChatMessage shutdownMsg = ChatMessage.System("Server is shutting down. Goodbye!");
        Broadcast(shutdownMsg);

        // Stop listener
        try
        {
            _listener?.Stop();
        }
        catch
        {
            // Ignore listener stop errors
        }

        // Dispose and clear all client sessions
        ClientSession[] remainingClients;
        lock (_clientsLock)
        {
            remainingClients = _clients.ToArray();
            _clients.Clear();
        }

        foreach (ClientSession client in remainingClients)
        {
            client.Dispose();
        }

        _listenerThread?.Join(1000);
        Console.WriteLine("[Server] Server stopped successfully.");
    }

    public void Dispose()
    {
        Stop();
    }
}
