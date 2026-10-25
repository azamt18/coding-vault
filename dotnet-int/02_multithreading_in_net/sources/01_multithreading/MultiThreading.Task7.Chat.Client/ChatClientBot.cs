using System.Net.Sockets;
using MultiThreading.Task7.Chat.Common;

namespace MultiThreading.Task7.Chat.Client;

public sealed class ChatClientBot
{
    private static readonly string[] PredefinedNames =
    {
        "Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ian", "Julia"
    };

    private static readonly string[] PredefinedMessages =
    {
        "Hello everyone! Hope you have a great sprint ahead.",
        "Can someone review PR #104 on the multithreading repo?",
        "Standup meeting starting in 5 minutes in Room 3.",
        "The deployment to staging succeeded with zero downtime.",
        "Reminder: Please update your task statuses on the board.",
        "Quick question: are we using ThreadPool or dedicated threads for this service?",
        "Don't forget to push your branch before the end of the day.",
        "Coffee break at the cafeteria if anyone wants to join!",
        "All matrix multiplication benchmarks passed successfully.",
        "Great work on resolving the race condition in the cache layer!"
    };

    private readonly string _host;
    private readonly int _port;
    private readonly Random _random = new();

    public ChatClientBot(string host = "127.0.0.1", int port = 5050)
    {
        _host = host;
        _port = port;
    }

    public void Run(CancellationToken cancellationToken)
    {
        Console.WriteLine($"[Bot Runner] Client Bot starting. Connecting to {_host}:{_port}...");

        int sessionIndex = 1;

        while (!cancellationToken.IsCancellationRequested)
        {
            string botName = $"{PredefinedNames[_random.Next(PredefinedNames.Length)]}-{_random.Next(100, 999)}";
            Console.WriteLine($"\n=======================================================");
            Console.WriteLine($"[Session #{sessionIndex++}] Starting session for bot '{botName}'");
            Console.WriteLine($"=======================================================");

            try
            {
                RunSingleSession(botName, cancellationToken);
            }
            catch (Exception ex) when (!cancellationToken.IsCancellationRequested)
            {
                Console.WriteLine($"[Bot Error] Session error: {ex.Message}. Retrying in 2 seconds...");
                Thread.Sleep(2000);
            }

            if (!cancellationToken.IsCancellationRequested)
            {
                int delayBeforeNextSessionMs = _random.Next(1000, 2500);
                Console.WriteLine($"[Bot Runner] Reconnecting with new identity in {delayBeforeNextSessionMs}ms...");
                Thread.Sleep(delayBeforeNextSessionMs);
            }
        }

        Console.WriteLine("[Bot Runner] Client Bot loop terminated.");
    }

    private sealed class BotSessionState
    {
        public volatile bool StopReceiving;
    }

    private void RunSingleSession(string botName, CancellationToken cancellationToken)
    {
        using var tcpClient = new TcpClient();
        tcpClient.Connect(_host, _port);
        using NetworkStream stream = tcpClient.GetStream();

        // 1. Handshake: Send Join message with bot name
        var joinMessage = ChatMessage.Join(botName);
        MessageFraming.WriteMessage(stream, joinMessage);
        Console.WriteLine($"[{botName}] Connected to server as '{botName}'.");

        // 2. Start background receiver thread
        var sessionState = new BotSessionState();
        Thread receiverThread = new Thread(() => ReceiveLoop(stream, botName, sessionState))
        {
            IsBackground = true,
            Name = $"{botName}-ReceiverThread"
        };
        receiverThread.Start();

        // 3. Send a random number of predefined messages with random delays
        int messageCount = _random.Next(3, 7);
        Console.WriteLine($"[{botName}] Scheduled to send {messageCount} messages.");

        for (int i = 0; i < messageCount && !cancellationToken.IsCancellationRequested; i++)
        {
            int delayMs = _random.Next(600, 1600);
            Thread.Sleep(delayMs);

            if (cancellationToken.IsCancellationRequested)
            {
                break;
            }

            string randomPhrase = PredefinedMessages[_random.Next(PredefinedMessages.Length)];
            var chatMsg = ChatMessage.Create(randomPhrase, botName);

            try
            {
                MessageFraming.WriteMessage(stream, chatMsg);
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
        sessionState.StopReceiving = true;

        try
        {
            var disconnectMsg = ChatMessage.Disconnect(botName);
            MessageFraming.WriteMessage(stream, disconnectMsg);
        }
        catch
        {
            // Ignore if server already closed
        }

        // Close stream to unblock any pending Read on receiver thread
        try
        {
            stream.Close();
            tcpClient.Close();
        }
        catch
        {
            // Ignore socket closure errors
        }

        receiverThread.Join(1000);
        Console.WriteLine($"[{botName}] Session ended.");
    }

    private static void ReceiveLoop(NetworkStream stream, string botName, BotSessionState sessionState)
    {
        try
        {
            while (!sessionState.StopReceiving)
            {
                ChatMessage? incoming = MessageFraming.ReadMessage(stream);
                if (incoming == null)
                {
                    break;
                }

                // Display incoming message on bot's screen/console
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
        catch (IOException)
        {
            // Stream closed on disconnect
        }
        catch (SocketException)
        {
            // Socket reset
        }
        catch (Exception ex) when (!sessionState.StopReceiving)
        {
            Console.WriteLine($"  << [{botName}] Error in receive loop: {ex.Message}");
        }
    }
}
