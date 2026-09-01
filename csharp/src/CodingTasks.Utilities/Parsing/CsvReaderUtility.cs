using System.Collections.Generic;
using System.IO;
using System.Text;
using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;

namespace CodingTasks.Utilities.Parsing;

public static class CsvReaderUtility
{
    public static List<T> ReadCsv<T>(string filePath)
    {
        using var reader = new StreamReader(filePath, Encoding.UTF8);
        using var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture));
        return new List<T>(csv.GetRecords<T>());
    }
}
