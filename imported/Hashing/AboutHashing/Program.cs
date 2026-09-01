// See https://aka.ms/new-console-template for more information

using System.Text;
using System.Diagnostics;

internal class Program
{
    private static void Main(string[] args)
    {
        // 3. sort in asc
        var hashes = new SortedSet<string>();

        // 1. reading files
        var files = Directory.EnumerateFiles(@"C:\Workspace\Other\itransition\task2\files");
        foreach (var file in files)
        {
            // 2. computing hash
            var input = File.ReadAllBytes(file);
            string hexString = HashUsingBouncyCastle(input);
            hashes.Add(hexString);
        }

        // 4. join hashes
        var joinedHash = string.Join("", hashes);

        // 5. concatenation
        joinedHash = string.Concat(joinedHash, "azam.turgunboyev@gmail.com");

        // 6. Find the SHA3-256 of the result string.
        {
            byte[] input = Encoding.ASCII.GetBytes(joinedHash);
            var hexString = HashUsingBouncyCastle(input);
            hexString = hexString.Replace("-", "").ToLowerInvariant();

            Console.WriteLine(hexString);
        }
    }

    public static string HashUsingBouncyCastle(byte[] input)
    {
        // Choose correct encoding based on your usecase
        var hashAlgorithm = new Org.BouncyCastle.Crypto.Digests.Sha3Digest(256);
        hashAlgorithm.BlockUpdate(input, 0, input.Length);

        byte[] result = new byte[32]; // 512 / 8 = 64
        hashAlgorithm.DoFinal(result, 0);

        string hashString = BitConverter.ToString(result);
        hashString = hashString.Replace("-", "").ToLowerInvariant();
        return hashString;
    }

    public static string LaunchCommandLineApp(string arguments)
    {
        string result = string.Empty;

        var proc = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "..\\..\\..\\..\\.\\computing_sha3_via_golang\\task2.exe",
                Arguments = arguments,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            }
        };

        proc.Start();
        while (!proc.StandardOutput.EndOfStream)
        {
            var readResult = proc.StandardOutput.ReadToEnd();
            result = readResult;
            // do something with line
        }

        return result;
    }
}