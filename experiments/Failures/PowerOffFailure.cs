using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{
    public class PowerOffFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly VirtualBox vbox;
        private string shutdownvm;

        public PowerOffFailure(IMongoDatabase db, VirtualBox vbox)
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
            this.vbox.ControlVM(this.shutdownvm, "poweroff");
        }
    }
}
