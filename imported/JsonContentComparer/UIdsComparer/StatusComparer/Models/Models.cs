using Newtonsoft.Json;

namespace UIdsComparer.StatusComparer.Models
{
    public enum InnerStatuses
    {
        ExecutorSigned = 10,
        CustomerAccepted = 11
    }

    public enum RoamingStatuses
    {
        ContractStatusExecutorSent = 15,
        ContractStatusExecutorCancel = 17,
        ContractStatusPartnerDecline = 20,
        ContractStatusPartnerAccept = 30
    }

    public class Id
    {
        [JsonProperty("$oid")] public string OId { get; set; }
    }

    public class DocumentMember
    {
        public string Inn { get; set; }
    }

    public class Contract
    {
        [JsonProperty("roaming_uid")]
        public string RoamingUid { get; set; }
    }

    public class DocumentModel
    {
        [JsonProperty("_id")] public Id Id { get; set; }
        public string Uid { get; set; }
        public DocumentMember Executor { get; set; }
        public DocumentMember Customer { get; set; }
        public InnerStatuses Status { get; set; }
        public Contract Contract { get; set; }
    }
}