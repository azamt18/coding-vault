using System.Net.Sockets;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Server;

public sealed class ClientSession : IDisposable
{
    private readonly object _writeLock = new();
    private bool _isDisposed;

    public ClientSession(Guid id, string clientName, TcpClient tcpClient)
    {
        Id = id;
        ClientName = clientName;
        TcpClient = tcpClient;
        Stream = tcpClient.GetStream();
    }

    public Guid Id { get; }
    public string ClientName { get; }
    public TcpClient TcpClient { get; }
    public NetworkStream Stream { get; }

    public bool IsConnected => TcpClient.Connected && !_isDisposed;

    public void Send(ChatMessage message)
    {
        if (_isDisposed)
        {
            return;
        }

        lock (_writeLock)
        {
            if (_isDisposed)
            {
                return;
            }

            MessageFraming.WriteMessage(Stream, message);
        }
    }

    public void Dispose()
    {
        if (_isDisposed)
        {
            return;
        }

        lock (_writeLock)
        {
            _isDisposed = true;
            try
            {
                Stream.Dispose();
                TcpClient.Dispose();
            }
            catch
            {
                // Ignore disposal errors on closing connections
            }
        }
    }
}
