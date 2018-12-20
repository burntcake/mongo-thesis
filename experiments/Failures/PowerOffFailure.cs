using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{
    public class PowerOffFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly EC2Client client;
        private string shutdownvm;

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
            this.shutdownvm = this.db.GetPrimaryReplica();
            this.client.terminateVM(this.shutdownvm);
        }
    }
}
