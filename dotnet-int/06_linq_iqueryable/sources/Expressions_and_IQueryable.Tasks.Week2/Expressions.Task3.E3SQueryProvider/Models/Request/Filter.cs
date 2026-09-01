using Newtonsoft.Json;
using System.Collections.Generic;

namespace Expressions.Task3.E3SQueryProvider.Models.Request
{
    [JsonObject]
    public class Filter
    {
        [JsonProperty("field")]
        public string Field { get; set; }

        [JsonProperty("values")]
        public List<string> Values { get; set; }
    }
}
