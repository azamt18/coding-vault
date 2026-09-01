using System;
using System.IO;
using System.Text;

namespace UIdsComparer.FilesFixer
{
    public class FilesFixer
    {
        public static void Run()
        {
            var rootFolder = new DirectoryInfo(@"c:\DOCROOT\services\contract-formation\attachments\");
            var stringBuilder = new StringBuilder();
            
            foreach (var innFolder in rootFolder.GetDirectories())
            {
                foreach (FileInfo fi in innFolder.GetFiles())
                {
                    Console.WriteLine(fi.Name + " " + fi.Length);

                    if (fi.Length == 0)
                    {
                        stringBuilder.Append($"Inn - {innFolder.Name}, Id - {fi.Name}, Length - {fi.Length}\n");
                    }
                }
            }

            File.WriteAllText(@"Files\empty_files.txt", stringBuilder.ToString());
        }
    }
}