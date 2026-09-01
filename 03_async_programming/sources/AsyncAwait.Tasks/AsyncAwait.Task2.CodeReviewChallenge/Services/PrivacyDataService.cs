using System.Threading.Tasks;

namespace AsyncAwait.Task2.CodeReviewChallenge.Services;

public class PrivacyDataService : IPrivacyDataService
{
    public Task<string> GetPrivacyDataAsync()
    {
        return new ValueTask<string>("This Policy describes how async/await processes your personal data," +
                                     "but it may not address all possible data processing scenarios.").AsTask();
    }
}
