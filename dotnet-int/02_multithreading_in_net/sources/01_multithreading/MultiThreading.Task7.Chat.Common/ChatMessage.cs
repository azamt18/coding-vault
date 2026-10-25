using System.Text.Json.Serialization;

namespace MultiThreading.Task7.Chat.Common;

public sealed record ChatMessage(
    [property: JsonPropertyName("id")] Guid Id,
    [property: JsonPropertyName("text")] string Text,
    [property: JsonPropertyName("sentAt")] DateTimeOffset SentAt,
    [property: JsonPropertyName("sentBy")] string SentBy,
    [property: JsonPropertyName("type")] ChatMessageType Type = ChatMessageType.Chat)
{
    public static ChatMessage Create(string text, string sentBy, ChatMessageType type = ChatMessageType.Chat) =>
        new(Guid.NewGuid(), text, DateTimeOffset.UtcNow, sentBy, type);

    public static ChatMessage Join(string clientName) =>
        Create($"{clientName} has joined the chat.", clientName, ChatMessageType.Join);

    public static ChatMessage Disconnect(string clientName) =>
        Create($"{clientName} has left the chat.", clientName, ChatMessageType.Disconnect);

    public static ChatMessage System(string text) =>
        Create(text, "SERVER", ChatMessageType.SystemNotification);
}
