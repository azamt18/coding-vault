namespace MultiThreading.Task7.Chat.Client;

internal static class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("=== Enterprise Chat Bot Client (Task 1: Synchronous Model) ===");
        string host = "127.0.0.1";
        int port = 5050;
        int botCount = 1;

        if (args.Length > 0 && int.TryParse(args[0], out int parsedPort))
        {
            port = parsedPort;
        }

        if (args.Length > 1 && int.TryParse(args[1], out int parsedBotCount))
        {
            botCount = Math.Max(1, parsedBotCount);
        }

        Console.WriteLine($"Target: {host}:{port} | Concurrent Bots: {botCount}");
        Console.WriteLine("Press Ctrl+C to stop the client bots.\n");

        using var cts = new CancellationTokenSource();

        Console.CancelKeyPress += (sender, eventArgs) =>
        {
            Console.WriteLine("\n[Shutdown] Stopping client bots...");
            eventArgs.Cancel = true;
            cts.Cancel();
        };

        if (botCount == 1)
        {
            var bot = new ChatClientBot(host, port);
            bot.Run(cts.Token);
        }
        else
        {
            // Run multiple bots concurrently
            var threads = new List<Thread>();
            for (int i = 0; i < botCount; i++)
            {
                int botIndex = i + 1;
                var thread = new Thread(() =>
                {
                    var bot = new ChatClientBot(host, port);
                    bot.Run(cts.Token);
                })
                {
                    IsBackground = true,
                    Name = $"BotWorkerThread-{botIndex}"
                };
                threads.Add(thread);
                thread.Start();
                Thread.Sleep(300); // Stagger initial starts slightly
            }

            foreach (var thread in threads)
            {
                thread.Join();
            }
        }

        Console.WriteLine("Client application exited.");
    }
}
