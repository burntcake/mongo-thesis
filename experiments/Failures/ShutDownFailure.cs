using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{

    public class ShutDownFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly VirtualBox vbox;

        private string shutdownvm;

        public ShutDownFailure(IMongoDatabase db, VirtualBox vbox)
        {
            this.db = db;
            this.vbox = vbox;
        }

        public void FixAsync()
        {
            this.vbox.StartVM(this.shutdownvm);
        }

        public void InduceAsync()
        {
            this.shutdownvm = this.db.GetPrimaryReplica();

            this.vbox.ControlVM(this.shutdownvm, "acpipowerbutton");
        }
    }
}
