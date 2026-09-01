using System.Net.Http;
using System.Threading.Tasks;

namespace CloudServices.Interfaces;

public interface ISupportService
{
    /// <summary>
    /// Registers the support request.
    /// </summary>
    /// <param name="requestInfo">The information about request.</param>
    /// <throws>
    ///     <exception cref="HttpRequestException">Emulated.</exception>
    /// </throws>
    /// <returns>The task.</returns>
    Task RegisterSupportRequestAsync(string requestInfo);

    /// <summary>
    /// Gets info about support request.
    /// </summary>
    /// <param name="requestInfo">The information about request.</param>
    /// <throws>
    ///     <exception cref="HttpRequestException">Emulated.</exception>
    /// </throws>
    /// <returns>The info about support request.</returns>
    Task<string> GetSupportInfoAsync(string requestInfo);
}
