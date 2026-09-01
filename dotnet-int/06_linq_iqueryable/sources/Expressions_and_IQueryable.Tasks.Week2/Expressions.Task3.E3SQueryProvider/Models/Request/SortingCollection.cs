using Expressions.Task3.E3SQueryProvider.Models.Request.Enums;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace Expressions.Task3.E3SQueryProvider.Models.Request
{
    [JsonDictionary]
    public class SortingCollection : Dictionary<string, SortOrder> { }
}
