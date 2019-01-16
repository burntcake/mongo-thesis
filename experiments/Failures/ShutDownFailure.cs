using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;
using System.Collections.Generic;

namespace MongoDBExperiments.Failures
{

    public class ShutDownFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly EC2Client client;

        private string shutdownvm;
        IDictionary<string, string> ec2InstanceId = new Dictionary<string, string>()
        {
            {"10.0.9.221", "i-0c292c6704cadd30c" },
            {"10.0.61.165", "i-00f83aff5af3fc9bd"},
            { "10.0.71.254", "i-0dca5b5dedac86a43"}
        };
        
        public ShutDownFailure(IMongoDatabase db, EC2Client client)
        {
            this.db = db;
            this.client = client;
        }

        public void FixAsync()
        {
            this.client.startVm(this.shutdownvm);
        }

        public void InduceAsync()
        {
            string result;
            if(ec2InstanceId.TryGetValue(db.GetPrimaryReplica(), out result))
            {
                this.shutdownvm = result;
            }

            this.client.stopVm(this.shutdownvm);
        }
    }
}
