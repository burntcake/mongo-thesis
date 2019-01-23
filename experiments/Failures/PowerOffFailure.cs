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
        private IDictionary<string, string> instanceIds;
      
        public PowerOffFailure(IMongoDatabase db, EC2Client client, IDictionary<string, string> instanceIds)
        {
            this.db = db;
            this.client = client;
            this.instanceIds = instanceIds;
        }

        public void FixAsync()
        {
            this.client.startVm(shutdownvm);
        }

        public void InduceAsync()
        {
            string result;
            if (instanceIds.TryGetValue(db.GetPrimaryReplica(), out result))
            {
                this.shutdownvm = result;
            }
            this.client.terminateVM(this.shutdownvm);
        }
    }
}
