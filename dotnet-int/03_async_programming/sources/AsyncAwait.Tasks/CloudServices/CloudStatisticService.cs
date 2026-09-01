using System.Collections.Concurrent;
using System.Threading.Tasks;
using CloudServices.Interfaces;

namespace CloudServices;

/// <summary>
/// This class emulates methods accessing to some cloud services.
/// No changes are needed here.
/// </summary>
public class CloudStatisticService : IStatisticService
{
    private static readonly ConcurrentDictionary<string, long> Statistics = new();

    /// <summary>
    /// Registers url visit in a Grand Statistic Storage cloud.
    /// </summary>
    /// <param name="url">The visited url.</param>
    public async Task RegisterVisitAsync(string url)
    {
        await Task.Delay(2000).ConfigureAwait(false); // emulation of long-running operation is here

        Statistics.AddOrUpdate(url, 1, (key, value) => value + 1);
    }

    /// <summary>
    /// Gets the amount of visits from Grand Statistic Storage cloud.
    /// </summary>
    /// <param name="url">The visited url.</param>
    /// <returns>The amount of registered visits.</returns>
    public async Task<long> GetVisitsCountAsync(string url)
    {
        await Task.Delay(100).ConfigureAwait(false); // emulation of long-running operation is here

        Statistics.TryGetValue(url, out var visits);
        return visits;
    }
}
