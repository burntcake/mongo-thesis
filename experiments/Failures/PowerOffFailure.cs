using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;
using System.Collections.Generic;
namespace MongoDBExperiments.Failures
{
    public class PowerOffFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly EC2Client client;
        private string shutdownvm;
        IDictionary<string, string> ec2InstanceId = new Dictionary<string, string>()
        {
            {"10.0.70.152", "i-02c28668c91630b9e" },
            {"10.0.21.232", "i-04e936fe73b7e4e9d"},
            { "10.0.50.226", "i-0a2540339b0b61499"}
        };
        public PowerOffFailure(IMongoDatabase db, EC2Client client)
        {
            this.db = db;
            this.client = client;
        }

        public void FixAsync()
        {
            this.client.startVm(shutdownvm);
        }

        public void InduceAsync()
        {
            string result;
            if (ec2InstanceId.TryGetValue(db.GetPrimaryReplica(), out result))
            {
                this.shutdownvm = result;
            }
            this.client.terminateVM(this.shutdownvm);
        }
    }
}
