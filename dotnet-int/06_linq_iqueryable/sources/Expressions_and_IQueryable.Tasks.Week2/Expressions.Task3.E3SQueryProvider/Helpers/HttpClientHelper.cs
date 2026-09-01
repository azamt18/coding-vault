using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;

namespace Expressions.Task3.E3SQueryProvider.Helpers
{
    public static class HttpClientHelper
    {
        public static HttpClient CreateClient(string userName, string password)
        {
            var client = new HttpClient(
                new HttpClientHandler
                {
                    AllowAutoRedirect = true,
                    PreAuthenticate = true
                });

            var encoding = new ASCIIEncoding();
            var authHeader = new AuthenticationHeaderValue(
                "Basic",
                Convert.ToBase64String(encoding.GetBytes($"{userName}:{password}")));
            client.DefaultRequestHeaders.Authorization = authHeader;

            return client;
        }
    }
}
