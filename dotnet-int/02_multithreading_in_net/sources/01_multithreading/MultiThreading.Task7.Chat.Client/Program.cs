namespace MultiThreading.Task7.Chat.Client;

internal static class Program
{
    private static async Task Main(string[] args)
    {
        Console.WriteLine("=================================================");
        Console.WriteLine("   ENTERPRISE CHAT CLIENT BOT (.NET 9 / TCP)     ");
        Console.WriteLine("=================================================");

        string mode = "async";
        string host = "127.0.0.1";
        int port = 5050;
        int botCount = 2;

        if (args.Length > 0)
        {
            if (args[0].Equals("sync", StringComparison.OrdinalIgnoreCase) || args[0].Equals("1", StringComparison.OrdinalIgnoreCase))
            {
                mode = "sync";
            }
            else if (args[0].Equals("async", StringComparison.OrdinalIgnoreCase) || args[0].Equals("2", StringComparison.OrdinalIgnoreCase))
            {
                mode = "async";
            }
        }

        if (args.Length > 1 && int.TryParse(args[1], out int parsedPort))
        {
            port = parsedPort;
        }

        if (args.Length > 2 && int.TryParse(args[2], out int parsedBotCount))
        {
            botCount = Math.Max(1, parsedBotCount);
        }

        Console.WriteLine($"[Mode] {mode.ToUpperInvariant()} | Target: {host}:{port} | Concurrent Bots: {botCount}");
        Console.WriteLine("Press Ctrl+C to stop the client bots.\n");

        using var cts = new CancellationTokenSource();

        Console.CancelKeyPress += (sender, eventArgs) =>
        {
            Console.WriteLine("\n[Shutdown] Stopping client bots...");
            eventArgs.Cancel = true;
            cts.Cancel();
        };

        if (mode == "sync")
        {
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
                    Name = $"SyncBotThread-{botIndex}"
                };
                threads.Add(thread);
                thread.Start();
                Thread.Sleep(200);
            }

            foreach (var thread in threads)
            {
                thread.Join();
            }
        }
        else
        {
            var botTasks = new List<Task>();
            for (int i = 0; i < botCount; i++)
            {
                var bot = new AsyncChatClientBot(host, port);
                botTasks.Add(bot.RunAsync(cts.Token));
                await Task.Delay(200, CancellationToken.None);
            }

            try
            {
                await Task.WhenAll(botTasks);
            }
            catch (OperationCanceledException)
            {
                // Normal exit
            }
        }

        Console.WriteLine("Client application exited.");
    }
}
