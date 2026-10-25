namespace MultiThreading.Task7.Chat.Server;

internal static class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("=== Enterprise Chat Server (Task 1: Thread-Per-Client Model) ===");
        int port = 5050;
        if (args.Length > 0 && int.TryParse(args[0], out int customPort))
        {
            port = customPort;
        }

        using var server = new ThreadPerClientChatServer(port);
        server.Start();

        var shutdownEvent = new ManualResetEventSlim(false);

        Console.CancelKeyPress += (sender, eventArgs) =>
        {
            Console.WriteLine("\n[Shutdown] Cancellation requested by user.");
            eventArgs.Cancel = true; // Prevent immediate brutal process termination
            shutdownEvent.Set();
        };

        Console.WriteLine("Server running. Press Ctrl+C or enter 'q' to stop.\n");

        while (!shutdownEvent.IsSet)
        {
            if (Console.KeyAvailable)
            {
                string? input = Console.ReadLine();
                if (input?.Trim().Equals("q", StringComparison.OrdinalIgnoreCase) == true)
                {
                    break;
                }
            }

            shutdownEvent.Wait(200);
        }

        server.Stop();
        Console.WriteLine("Server exit complete.");
    }
}
