using System;
using System.IO;
using System.Linq;

namespace Renamer
{
    class Program
    {
        static void Main(string[] args)
        {
            var productionAdress = "https://bizpayment.micro.faktura.uz/";
            var stagingAdress = "https://stage.micro.faktura.uz/bizpayment/";



            var SubPositionName = "";
            var BrandName = "str2";
            var AttributeName = "str3";

            var stringsArray = new[] { SubPositionName, BrandName, AttributeName };
            var solution3 = stringsArray.Where(x => !string.IsNullOrEmpty(x)).Aggregate((i, j) => i + " " + j);

            var solution4 = string.Join(' ', SubPositionName, BrandName, AttributeName);
            var solution5 = string.Join(' ', stringsArray.Where(s => !string.IsNullOrEmpty(s)));

            // The files used in this example are created in the topic
            // How to: Write to a Text File. You can change the path and
            // file name to substitute text files of your own.

            // Example #1
            // Read the file as one string.
            //string text = System.IO.File.ReadAllText(@"C:\Users\Fathulla\OneDrive\Pochta\tasks\osm\mails.txt");

            // Display the file contents to the console. Variable text is a string.
            //System.Console.WriteLine("Contents of WriteText.txt = {0}", text);

            // Example #2
            // Read each line of the file into a string array. Each element
            // of the array is one line of the file.
            string[] lines = System.IO.File.ReadAllLines(@"C:\Users\Fathulla\OneDrive\Pochta\tasks\osm\mails.txt");

            var g = lines.GroupBy(x => x).Select(x => new
                {
                    uid = x.Key,
                    count = x.Count()
                })
                .ToArray();

            var a1 = g.Where(x => x.count == 1).ToArray();
            var a2 = g.Where(x => x.count > 1).ToArray();
            var s = g.Sum(x => x.count);

            // Keep the console window open in debug mode.
            Console.WriteLine("Press any key to exit.");
            System.Console.ReadKey();
        }
    }
}
