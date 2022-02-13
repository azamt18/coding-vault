using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parser
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                var streamReader = File.ReadAllLines("../../data.txt", Encoding.UTF8);
                var linesList = new List<string>();
                foreach (var line in streamReader)
                {
                    var items = line
                        .Replace('\'', '`')
                        .Replace('‘', '`')
                        .Replace('“', '\"')
                        .Replace('”', '\"')
                        .Split('\t');
                    var organName = items[0];
                    var unitName = string.IsNullOrEmpty(items[1]) ? string.Empty : $" {items[1]}";
                    var region = string.IsNullOrEmpty(items[2]) ? string.Empty : $", {items[2]}";
                    var area = string.IsNullOrEmpty(items[3]) ? string.Empty : $", {items[3]}";
                    var code = items[4];
                    var currentLine = $"(N'{organName}{unitName}{region}{area}', 10, '{code}')";
                    linesList.Add(currentLine);
                }

                var sb = new StringBuilder();
                while (true)
                {
                    var valuesList = linesList.Take(1000).ToList();
                    if (!valuesList.Any())
                        break;
                    linesList = linesList.Skip(1000).ToList();

                    sb.AppendLine("INSERT INTO [ClientUnit]([Name],[ClientType],[ClientCode]) VALUES ");
                    var count = 0;
                    foreach (var value in valuesList)
                    {
                        count++;
                        var append = count == valuesList.Count ? string.Empty : ",";
                        sb.AppendLine($"{value}{append}");
                    }
                }

                File.WriteAllText("../../insert_query.txt", sb.ToString());
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                throw;
            }
        }
    }
}
