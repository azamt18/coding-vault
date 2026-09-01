using System.Diagnostics;

namespace UIdsComparer
{
    internal static class Program
    {
        private static void Main(string[] args)
        {
            var program = new StatusComparer.StatusComparer();
            program.Run();
        }
    }
}
