using System;
using System.Data.OleDb;

namespace Parser.Excel
{
    public static class ExcelReader
    {
        private const string Path = @"c:\Workspace\Other\Parser\Parser\bin\Debug\GAI_ADDRESS_20230110.xlsx";
        private static readonly string ConnectionString = $@"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={Path};" + @"Extended Properties='Excel 8.0;HDR=Yes;'";

        public static void Parse()
        {
            using(OleDbConnection connection = new OleDbConnection(ConnectionString))
            {
                connection.Open();
                OleDbCommand command = new OleDbCommand("select * from [Sheet1$]", connection); 
                using(OleDbDataReader dataReader = command.ExecuteReader())
                {
                    while(dataReader.Read())
                    {
                        var address = dataReader[0];
                        var postIndex = dataReader[1];
                        Console.WriteLine($"{address}   {postIndex}");
                    }
                }
            }
        }
    }
}