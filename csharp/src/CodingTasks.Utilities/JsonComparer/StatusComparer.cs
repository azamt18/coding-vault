using System;
using System.Collections.Generic;
using System.Linq;

namespace CodingTasks.Utilities.JsonComparer;

public class StatusRecord
{
    public string Uid { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
}

public static class StatusComparer
{
    public static List<string> FindDiscrepancies(IEnumerable<StatusRecord> first, IEnumerable<StatusRecord> second)
    {
        var firstMap = first.ToDictionary(r => r.Uid, r => r.Status);
        var secondMap = second.ToDictionary(r => r.Uid, r => r.Status);

        var discrepancies = new List<string>();

        foreach (var (uid, status) in firstMap)
        {
            if (secondMap.TryGetValue(uid, out var otherStatus) && status != otherStatus)
            {
                discrepancies.Add($"UID {uid}: Status '{status}' != '{otherStatus}'");
            }
        }

        return discrepancies;
    }
}
