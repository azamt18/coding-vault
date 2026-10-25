namespace MultiThreading.Task7.Chat.Server;

internal static class Program
{
    private static async Task Main(string[] args)
    {
        Console.WriteLine("=================================================");
        Console.WriteLine("    ENTERPRISE CHAT SERVER (.NET 9 / Sockets)    ");
        Console.WriteLine("=================================================");

        string mode = "async"; // Default to modern Task 2 async
        int port = 5050;

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
            else if (int.TryParse(args[0], out int parsedPort))
            {
                port = parsedPort;
            }
        }

        if (args.Length > 1 && int.TryParse(args[1], out int parsedPort2))
        {
            port = parsedPort2;
        }

        using var cts = new CancellationTokenSource();

        Console.CancelKeyPress += (sender, eventArgs) =>
        {
            Console.WriteLine("\n[Shutdown] Stopping server...");
            eventArgs.Cancel = true;
            cts.Cancel();
        };

        if (mode == "sync")
        {
            Console.WriteLine($"[Mode] Running Task 1: Synchronous Thread-Per-Client Model on port {port}.");
            using var syncServer = new ThreadPerClientChatServer(port);
            syncServer.Start();
            Console.WriteLine("Press Ctrl+C to stop.\n");

            try
            {
                await Task.Delay(Timeout.Infinite, cts.Token);
            }
            catch (OperationCanceledException)
            {
                // Normal exit
            }

            syncServer.Stop();
        }
        else
        {
            Console.WriteLine($"[Mode] Running Task 2: Asynchronous TPL & Channels Model on port {port}.");
            var asyncServer = new AsyncChatServer(port);
            asyncServer.Start();
            Console.WriteLine("Press Ctrl+C to stop.\n");

            try
            {
                await Task.Delay(Timeout.Infinite, cts.Token);
            }
            catch (OperationCanceledException)
            {
                // Normal exit
            }

            await asyncServer.StopAsync();
        }

        Console.WriteLine("Server exit complete.");
    }
}
