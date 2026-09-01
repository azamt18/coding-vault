using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UIdsComparer.StatusComparer.Models;

namespace UIdsComparer.StatusComparer
{
    
    public class StatusComparer
    {
        // here and other keys/domains have been changed to fake data
        private const string ClientId = "fakeClientId";
        private const string ClientSecret = "fakeClientSecret";

        public void Run()
        {
            var client = new HttpClient();
            client.BaseAddress = new Uri("https://fakeaddress.com");
            var authenticationString = $"{ClientId}:{ClientSecret}";
            var base64EncodedAuthenticationString = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes(authenticationString));
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", base64EncodedAuthenticationString);

            var documents = JArray.Parse(File.ReadAllText(@"..\..\StatusComparer\Files\a.json"));
            
            var counter = 0;
            var okDocuments = new StringBuilder();
            var conflictDocuments = new StringBuilder();
            
            foreach (var document in documents)
            {
                var obj = JsonConvert.DeserializeObject<DocumentModel>(document.ToString());
                if (obj != null)
                {

                    Console.WriteLine($"{++counter}. {obj.Id} - {obj.Uid} - {obj.Contract.RoamingUid} {obj.Executor.Inn} {obj.Customer.Inn}");
                    
                    var response = client.GetAsync($"/provider/api/ru/{obj?.Customer.Inn}/contracts/client/{obj?.Contract.RoamingUid}").Result;
                    if (!response.IsSuccessStatusCode)
                    {
                        response = client.GetAsync($"/provider/api/ru/{obj?.Executor.Inn}/contracts/owner/{obj?.Contract.RoamingUid}").Result;
                    }

                    if (response.IsSuccessStatusCode)
                    {
                        var content = response.Content.ReadAsStringAsync().Result;
                        JObject result = JObject.Parse(content);
                        var currentStateId = (int) result["currentStateId"];
                        var clientStateId = (int) result["clientStateId"];


                        var innerStatus = obj.Status == InnerStatuses.ExecutorSigned ? 15 : 30;

                        if (innerStatus == currentStateId)
                            okDocuments.Append($"Id - {obj.Id.OId}, Uid - {obj.Uid}, RoamingUid - {obj.Contract.RoamingUid} = executor {obj.Executor.Inn} status(inner/roaming): {innerStatus} / {currentStateId}; customer {obj.Customer.Inn} status(inner/roaming): {innerStatus} / {clientStateId}\n");
                        else
                            conflictDocuments.Append($"{obj.Contract.RoamingUid} {obj.Executor.Inn}\n"); 
                    }
                    else
                    {
                        var text = $"Id - {obj.Id.OId}, Uid - {obj.Uid}, RoamingUid - {obj.Contract.RoamingUid} = {response.Content.ReadAsStringAsync().Result}";
                        File.WriteAllText(@"..\..\StatusComparer\Files\status_compare_error_result.txt", text);
                    }
                }
            }

            File.WriteAllText(@"..\..\StatusComparer\Files\status_compare_ok.txt", okDocuments.ToString()); 
            File.WriteAllText(@"..\..\StatusComparer\Files\status_compare_conflict_uids.txt", conflictDocuments.ToString()); 
        }
    }
}