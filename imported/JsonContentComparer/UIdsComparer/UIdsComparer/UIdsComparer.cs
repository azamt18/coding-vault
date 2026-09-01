using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Comparer.UIdsComparer
{
    public class RootObject
    {
        public List<string> UniqueIds { get; set; }
    }

    public class UIdsComparer
    {
        public void Run()
        {
            JObject getCompanyDocumentUids = JObject.Parse(File.ReadAllText(@"..\..\GetCompanyDocumentUids.json"));
            JObject getDocuments = JObject.Parse(File.ReadAllText(@"..\..\GetDocuments.json"));

            if (getCompanyDocumentUids.ContainsKey("UniqueIds") && getDocuments.ContainsKey("UniqueIds"))
            {
                // 1st: find uniqueId that is in GetCompanyDocumentUids, but not in GetDocuments
                {
                    var notIncludedUids = new RootObject { UniqueIds = new List<string>() };
                    var getCompanyDocumentUidsArray = JsonConvert.DeserializeObject<RootObject>(getCompanyDocumentUids.ToString())?.UniqueIds;
                    var getDocumentsArray = JsonConvert.DeserializeObject<RootObject>(getDocuments.ToString())?.UniqueIds;

                    if (getCompanyDocumentUidsArray != null && getDocumentsArray != null)
                    {
                        foreach (var item in getCompanyDocumentUidsArray)
                        {
                            if (!getDocumentsArray.Contains(item))
                            {
                                notIncludedUids.UniqueIds.Add(item);
                            }
                        }
                    }

                    File.WriteAllText(@"..\..\GetCompanyDocumentUidsNotIncludedInGetDocuments.json", JsonConvert.SerializeObject(notIncludedUids));
                }

                // 2nd: find uniqueId that is in GetDocuments, but not in GetCompanyDocumentUids
                {
                    var notIncludedUids = new RootObject() { UniqueIds = new List<string>() };
                    var getDocumentsArray = JsonConvert.DeserializeObject<RootObject>(getDocuments.ToString())?.UniqueIds;
                    var getCompanyDocumentUidsArray = JsonConvert.DeserializeObject<RootObject>(getCompanyDocumentUids.ToString())?.UniqueIds;

                    if (getDocumentsArray != null && getCompanyDocumentUidsArray != null)
                    {
                        foreach (var item in getDocumentsArray)
                        {
                            if (!getCompanyDocumentUidsArray.Contains(item))
                            {
                                notIncludedUids.UniqueIds.Add(item);
                            }
                        }
                    }

                    File.WriteAllText(@"..\..\GetDocumentsUidsNotIncludedInGetCompanyDocumentUids.json", JsonConvert.SerializeObject(notIncludedUids));
                }
            }

        }
    }
}