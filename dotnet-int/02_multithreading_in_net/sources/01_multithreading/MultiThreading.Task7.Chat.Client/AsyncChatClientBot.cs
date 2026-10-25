using System.Net.Sockets;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Client;

public sealed class AsyncChatClientBot
{
    private static readonly string[] PredefinedNames =
    {
        "Async-Alice", "Async-Bob", "Async-Charlie", "Async-Diana", "Async-Evan",
        "Async-Fiona", "Async-George", "Async-Hannah", "Async-Ian", "Async-Julia"
    };

    private static readonly string[] PredefinedMessages =
    {
        "Async I/O scales gracefully without holding OS thread stacks.",
        "Testing throughput with TPL and System.Threading.Channels.",
        "Non-blocking stream writes completed with zero lock contention.",
        "All async background workers yielded their threads back to the ThreadPool.",
        "Channel reader drained outbound messages asynchronously.",
        "Task.WhenAll completed message delivery across all active sessions.",
        "Verified IOCP completion callbacks under heavy simulated traffic.",
        "TPL makes concurrent socket operations both efficient and expressive."
    };

    private readonly string _host;
    private readonly int _port;
    private readonly Random _random = new();

    public AsyncChatClientBot(string host = "127.0.0.1", int port = 5050)
    {
        _host = host;
        _port = port;
    }

    public async Task RunAsync(CancellationToken cancellationToken)
    {
        Console.WriteLine($"[AsyncBot Runner] Starting async bot against {_host}:{_port}...");
        int sessionIndex = 1;

        while (!cancellationToken.IsCancellationRequested)
        {
            string botName = $"{PredefinedNames[_random.Next(PredefinedNames.Length)]}-{_random.Next(100, 999)}";
            Console.WriteLine($"\n=======================================================");
            Console.WriteLine($"[Async Session #{sessionIndex++}] Starting session for '{botName}'");
            Console.WriteLine($"=======================================================");

            try
            {
                await RunSingleSessionAsync(botName, cancellationToken).ConfigureAwait(false);
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[AsyncBot Error] Session error: {ex.Message}. Retrying in 2 seconds...");
                await Task.Delay(2000, cancellationToken).ConfigureAwait(false);
            }

            if (!cancellationToken.IsCancellationRequested)
            {
                int delayBeforeNextSessionMs = _random.Next(1000, 2500);
                Console.WriteLine($"[AsyncBot Runner] Reconnecting in {delayBeforeNextSessionMs}ms...");
                await Task.Delay(delayBeforeNextSessionMs, cancellationToken).ConfigureAwait(false);
            }
        }

        Console.WriteLine("[AsyncBot Runner] Bot loop terminated.");
    }

    private async Task RunSingleSessionAsync(string botName, CancellationToken cancellationToken)
    {
        using var tcpClient = new TcpClient();
        await tcpClient.ConnectAsync(_host, _port, cancellationToken).ConfigureAwait(false);
        using NetworkStream stream = tcpClient.GetStream();

        // 1. Handshake
        var joinMessage = ChatMessage.Join(botName);
        await MessageFraming.WriteMessageAsync(stream, joinMessage, cancellationToken).ConfigureAwait(false);
        Console.WriteLine($"[{botName}] Connected to server as '{botName}'.");

        // 2. Start background receiver task
        using var sessionCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        Task receiveTask = ReceiveLoopAsync(stream, botName, sessionCts.Token);

        // 3. Send random predefined messages with async delays
        int messageCount = _random.Next(3, 7);
        Console.WriteLine($"[{botName}] Scheduled to send {messageCount} messages.");

        for (int i = 0; i < messageCount && !cancellationToken.IsCancellationRequested; i++)
        {
            int delayMs = _random.Next(600, 1600);
            await Task.Delay(delayMs, cancellationToken).ConfigureAwait(false);

            if (cancellationToken.IsCancellationRequested)
            {
                break;
            }

            string randomPhrase = PredefinedMessages[_random.Next(PredefinedMessages.Length)];
            var chatMsg = ChatMessage.Create(randomPhrase, botName);

            try
            {
                await MessageFraming.WriteMessageAsync(stream, chatMsg, cancellationToken).ConfigureAwait(false);
                Console.WriteLine($"[{botName} >> Sent] {randomPhrase}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[{botName}] Send failed: {ex.Message}");
                break;
            }
        }

        // 4. Graceful Disconnect
        Console.WriteLine($"[{botName}] Finished message quota. Disconnecting...");
        sessionCts.Cancel();

        try
        {
            var disconnectMsg = ChatMessage.Disconnect(botName);
            await MessageFraming.WriteMessageAsync(stream, disconnectMsg, CancellationToken.None).ConfigureAwait(false);
        }
        catch
        {
            // Ignore if server already closed
        }

        try
        {
            stream.Close();
            tcpClient.Close();
        }
        catch
        {
            // Ignore socket closure errors
        }

        try
        {
            await receiveTask.ConfigureAwait(false);
        }
        catch
        {
            // Ignore receiver task exceptions on disconnection
        }

        Console.WriteLine($"[{botName}] Session ended.");
    }

    private static async Task ReceiveLoopAsync(NetworkStream stream, string botName, CancellationToken cancellationToken)
    {
        try
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                ChatMessage? incoming = await MessageFraming.ReadMessageAsync(stream, cancellationToken).ConfigureAwait(false);
                if (incoming == null)
                {
                    break;
                }

                string time = incoming.SentAt.ToLocalTime().ToString("HH:mm:ss");
                string tag = incoming.Type switch
                {
                    ChatMessageType.History => "[HISTORY]",
                    ChatMessageType.SystemNotification => "[SYSTEM]",
                    ChatMessageType.Join => "[JOIN]",
                    ChatMessageType.Disconnect => "[LEAVE]",
                    _ => $"[{incoming.SentBy}]"
                };

                Console.WriteLine($"  << [{botName} Screen @ {time}] {tag} {incoming.Text}");
            }
        }
        catch (OperationCanceledException)
        {
            // Expected on cancellation
        }
        catch (IOException)
        {
            // Socket closed
        }
        catch (SocketException)
        {
            // Socket reset
        }
        catch (Exception ex)
        {
            Console.WriteLine($"  << [{botName}] Error in receive loop: {ex.Message}");
        }
    }
}
