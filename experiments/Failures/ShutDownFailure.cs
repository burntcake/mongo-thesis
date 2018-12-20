using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{

    public class ShutDownFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly EC2Client client;

        private string shutdownvm;

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
            this.shutdownvm = this.db.GetPrimaryReplica();

            this.client.stopVm(this.shutdownvm);
        }
    }
}
