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
        private IDictionary<string, string> instanceIds;
        
        public ShutDownFailure(IMongoDatabase db, EC2Client client, IDictionary<string, string> instanceIds)
        {
            this.db = db;
            this.client = client;
            this.instanceIds = instanceIds;
        }

        public void FixAsync()
        {
            this.client.startVm(this.shutdownvm);
        }

        public void InduceAsync()
        {
            this.shutdownvm = db.GetPrimaryReplica();
            this.client.stopVm(this.shutdownvm);
        }
    }
}
