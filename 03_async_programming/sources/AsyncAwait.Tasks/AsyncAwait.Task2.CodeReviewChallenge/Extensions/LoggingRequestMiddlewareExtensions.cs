using AsyncAwait.Task2.CodeReviewChallenge.Middleware;
using Microsoft.AspNetCore.Builder;

namespace AsyncAwait.Task2.CodeReviewChallenge.Extensions;

public static class LoggingRequestMiddlewareExtensions
{
    public static IApplicationBuilder UseStatistic(this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<StatisticMiddleware>();
    }
}
