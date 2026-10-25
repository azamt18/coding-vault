using System.Buffers.Binary;
using System.Net.Sockets;
using System.Text.Json;

namespace MultiThreading.Task7.Chat.Common;

public static class MessageFraming
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    public static void WriteMessage(Stream stream, ChatMessage message)
    {
        ArgumentNullException.ThrowIfNull(stream);
        ArgumentNullException.ThrowIfNull(message);

        byte[] payloadBytes = JsonSerializer.SerializeToUtf8Bytes(message, JsonOptions);
        Span<byte> lengthPrefix = stackalloc byte[4];
        BinaryPrimitives.WriteInt32LittleEndian(lengthPrefix, payloadBytes.Length);

        stream.Write(lengthPrefix);
        stream.Write(payloadBytes);
        stream.Flush();
    }

    public static ChatMessage? ReadMessage(Stream stream)
    {
        ArgumentNullException.ThrowIfNull(stream);

        byte[] lengthBuffer = new byte[4];
        if (!TryReadExact(stream, lengthBuffer))
        {
            return null; // Remote endpoint closed connection
        }

        int payloadLength = BinaryPrimitives.ReadInt32LittleEndian(lengthBuffer);
        if (payloadLength < 0 || payloadLength > 10 * 1024 * 1024) // 10MB sanity limit
        {
            throw new InvalidOperationException($"Invalid message payload length: {payloadLength} bytes.");
        }

        byte[] payloadBuffer = new byte[payloadLength];
        if (!TryReadExact(stream, payloadBuffer))
        {
            return null; // Connection closed mid-message
        }

        return JsonSerializer.Deserialize<ChatMessage>(payloadBuffer, JsonOptions);
    }

    public static async Task WriteMessageAsync(Stream stream, ChatMessage message, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(stream);
        ArgumentNullException.ThrowIfNull(message);

        byte[] payloadBytes = JsonSerializer.SerializeToUtf8Bytes(message, JsonOptions);
        byte[] lengthPrefix = new byte[4];
        BinaryPrimitives.WriteInt32LittleEndian(lengthPrefix, payloadBytes.Length);

        await stream.WriteAsync(lengthPrefix, cancellationToken).ConfigureAwait(false);
        await stream.WriteAsync(payloadBytes, cancellationToken).ConfigureAwait(false);
        await stream.FlushAsync(cancellationToken).ConfigureAwait(false);
    }

    public static async Task<ChatMessage?> ReadMessageAsync(Stream stream, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(stream);

        byte[] lengthBuffer = new byte[4];
        bool hasReadLength = await TryReadExactAsync(stream, lengthBuffer, cancellationToken).ConfigureAwait(false);
        if (!hasReadLength)
        {
            return null;
        }

        int payloadLength = BinaryPrimitives.ReadInt32LittleEndian(lengthBuffer);
        if (payloadLength < 0 || payloadLength > 10 * 1024 * 1024)
        {
            throw new InvalidOperationException($"Invalid message payload length: {payloadLength} bytes.");
        }

        byte[] payloadBuffer = new byte[payloadLength];
        bool hasReadPayload = await TryReadExactAsync(stream, payloadBuffer, cancellationToken).ConfigureAwait(false);
        if (!hasReadPayload)
        {
            return null;
        }

        return JsonSerializer.Deserialize<ChatMessage>(payloadBuffer, JsonOptions);
    }

    private static bool TryReadExact(Stream stream, byte[] buffer)
    {
        int totalBytesRead = 0;
        while (totalBytesRead < buffer.Length)
        {
            int bytesRead = stream.Read(buffer, totalBytesRead, buffer.Length - totalBytesRead);
            if (bytesRead == 0)
            {
                return false;
            }
            totalBytesRead += bytesRead;
        }
        return true;
    }

    private static async Task<bool> TryReadExactAsync(Stream stream, byte[] buffer, CancellationToken cancellationToken)
    {
        int totalBytesRead = 0;
        while (totalBytesRead < buffer.Length)
        {
            int bytesRead = await stream.ReadAsync(buffer.AsMemory(totalBytesRead, buffer.Length - totalBytesRead), cancellationToken).ConfigureAwait(false);
            if (bytesRead == 0)
            {
                return false;
            }
            totalBytesRead += bytesRead;
        }
        return true;
    }
}
