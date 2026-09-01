using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using Expressions.Task3.E3SQueryProvider.Helpers;
using Expressions.Task3.E3SQueryProvider.Models.Entities;
using Expressions.Task3.E3SQueryProvider.QueryProvider;
using Expressions.Task3.E3SQueryProvider.Services;
using Microsoft.Extensions.Configuration;
using Xunit;
using Xunit.Abstractions;

namespace Expressions.Task3.E3SQueryProvider.Test.Ignored
{
    /// <summary>
    /// Please ignore this integration test set, because the E3S emulator is not currently available.
    /// </summary>
    public class E3SProviderTests
    {
        #region private 

        private readonly ITestOutputHelper _testOutputHelper;

        private static IConfigurationRoot config = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json")
            .Build();

        private static string User = config["api:user"];
        private static string Password = config["api:password"];
        private static string BaseUrl = config["api:apiBaseUrl"];

        private static readonly Lazy<E3SSearchService> searchService = new Lazy<E3SSearchService>(() =>
        {
            HttpClient httpClient = HttpClientHelper.CreateClient(User, Password);
            return new E3SSearchService(httpClient, BaseUrl);
        });

        #endregion

        public E3SProviderTests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
        }

        #region public tests

        [Fact(Skip = "This test is provided to show the general idea of usage.")]
        public void WithoutProvider()
        {
            IEnumerable<EmployeeEntity> res = searchService.Value.SearchFts<EmployeeEntity>("workstation:(EPRUIZHW0249)", 0, 1);

            foreach (var emp in res)
            {
                _testOutputHelper.WriteLine("{0} {1}", emp.NativeName, emp.StartWorkDate);
            }
        }

        [Fact(Skip = "This test is provided to show the general idea of usage.")]
        public void WithoutProviderNonGeneric()
        {
            var res = searchService.Value.SearchFts(typeof(EmployeeEntity), "workstation:(EPRUIZHW0249)", 0, 10);

            foreach (var emp in res.OfType<EmployeeEntity>())
            {
                _testOutputHelper.WriteLine("{0} {1}", emp.NativeName, emp.StartWorkDate);
            }
        }

        [Fact(Skip = "This test is provided to show the general idea of usage.")]
        public void WithProvider()
        {
            var employees = new E3SEntitySet<EmployeeEntity>(searchService.Value);

            foreach (var emp in employees.Where(e => e.Workstation == "EPRUIZHW0249"))
            {
                _testOutputHelper.WriteLine("{0} {1}", emp.NativeName, emp.StartWorkDate);
            }
        }

        #endregion
    }
}
