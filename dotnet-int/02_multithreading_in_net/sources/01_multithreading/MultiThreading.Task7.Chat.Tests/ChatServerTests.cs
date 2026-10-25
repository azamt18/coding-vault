using System.Net.Sockets;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using MultiThreading.Task7.Chat.Common;
using MultiThreading.Task7.Chat.Server;

namespace MultiThreading.Task7.Chat.Tests;

[TestClass]
public sealed class ChatServerTests
{
    private static int GetAvailablePort()
    {
        using var listener = new TcpListener(System.Net.IPAddress.Loopback, 0);
        listener.Start();
        int port = ((System.Net.IPEndPoint)listener.LocalEndpoint).Port;
        listener.Stop();
        return port;
    }

    [TestMethod]
    public void BoundedMessageHistory_ShouldRetainOnlyLastNCapacity()
    {
        var history = new BoundedMessageHistory(capacity: 3);

        for (int i = 1; i <= 5; i++)
        {
            history.Add(ChatMessage.Create($"Message {i}", "Author"));
        }

        IReadOnlyList<ChatMessage> recent = history.GetRecentMessages();
        Assert.AreEqual(3, recent.Count);
        Assert.AreEqual("Message 3", recent[0].Text);
        Assert.AreEqual("Message 4", recent[1].Text);
        Assert.AreEqual("Message 5", recent[2].Text);
    }

    [TestMethod]
    public async Task SynchronousServer_ShouldBroadcastMessages_AndReplayHistory()
    {
        int port = GetAvailablePort();
        using var server = new ThreadPerClientChatServer(port, historyCapacity: 5);
        server.Start();

        // 1. Connect Client 1 (Alice)
        using var client1 = new TcpClient();
        await client1.ConnectAsync("127.0.0.1", port);
        NetworkStream stream1 = client1.GetStream();
        MessageFraming.WriteMessage(stream1, ChatMessage.Join("Alice"));

        // 2. Client 1 sends a message
        var msg1 = ChatMessage.Create("Hello from Alice!", "Alice");
        MessageFraming.WriteMessage(stream1, msg1);

        // Give server a moment to process & save to history
        await Task.Delay(150);

        // 3. Connect Client 2 (Bob)
        using var client2 = new TcpClient();
        await client2.ConnectAsync("127.0.0.1", port);
        NetworkStream stream2 = client2.GetStream();
        MessageFraming.WriteMessage(stream2, ChatMessage.Join("Bob"));

        // 4. Bob should receive historical messages (Join notice + Alice's message)
        ChatMessage? hist1 = MessageFraming.ReadMessage(stream2);
        ChatMessage? hist2 = MessageFraming.ReadMessage(stream2);

        Assert.IsNotNull(hist1);
        Assert.IsNotNull(hist2);
        Assert.IsTrue(hist1.Text.Contains("Alice has joined") || hist1.Text.Contains("Hello from Alice"));
        Assert.IsTrue(hist2.Text.Contains("Alice has joined") || hist2.Text.Contains("Hello from Alice"));

        // 5. Alice should receive Bob's join notification
        ChatMessage? joinNotification = MessageFraming.ReadMessage(stream1);
        Assert.IsNotNull(joinNotification);
        Assert.IsTrue(joinNotification.Text.Contains("Bob has joined"));

        server.Stop();
    }

    [TestMethod]
    public async Task AsyncServer_ShouldBroadcastMessages_AndReplayHistory()
    {
        int port = GetAvailablePort();
        await using var server = new AsyncChatServer(port, historyCapacity: 5);
        server.Start();

        // 1. Connect Client 1 (Charlie)
        using var client1 = new TcpClient();
        await client1.ConnectAsync("127.0.0.1", port);
        NetworkStream stream1 = client1.GetStream();
        await MessageFraming.WriteMessageAsync(stream1, ChatMessage.Join("Charlie"));

        // 2. Charlie sends a message
        var msg1 = ChatMessage.Create("Async pipeline working!", "Charlie");
        await MessageFraming.WriteMessageAsync(stream1, msg1);

        await Task.Delay(150);

        // 3. Connect Client 2 (Diana)
        using var client2 = new TcpClient();
        await client2.ConnectAsync("127.0.0.1", port);
        NetworkStream stream2 = client2.GetStream();
        await MessageFraming.WriteMessageAsync(stream2, ChatMessage.Join("Diana"));

        // 4. Diana receives history
        ChatMessage? hist1 = await MessageFraming.ReadMessageAsync(stream2);
        ChatMessage? hist2 = await MessageFraming.ReadMessageAsync(stream2);

        Assert.IsNotNull(hist1);
        Assert.IsNotNull(hist2);

        // 5. Charlie receives Diana's join notification
        ChatMessage? joinNotice = await MessageFraming.ReadMessageAsync(stream1);
        Assert.IsNotNull(joinNotice);
        Assert.IsTrue(joinNotice.Text.Contains("Diana has joined"));

        await server.StopAsync();
    }
}
