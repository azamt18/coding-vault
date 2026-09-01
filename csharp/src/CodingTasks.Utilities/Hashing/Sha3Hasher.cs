using System;
using System.Diagnostics;
using System.Text;
using System.Security.Cryptography;

namespace CodingTasks.Utilities.Hashing;

public static class Sha3Hasher
{
    public static string ComputeSha256(byte[] input)
    {
        var hash = SHA256.HashData(input);
        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    public static string ComputeSha256(string input)
    {
        return ComputeSha256(Encoding.UTF8.GetBytes(input));
    }
}
