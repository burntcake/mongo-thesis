using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{
    public class ImmutableDiskFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly VirtualBox vbox;

        private string shutdownvm;

        public ImmutableDiskFailure(IMongoDatabase db, VirtualBox vbox)
        {
            this.db = db;
            this.vbox = vbox;
        }

        public Task FixAsync()
        {
            this.ChangeDiskState(this.shutdownvm, "normal");
            return Task.CompletedTask;
        }

        public async Task InduceAsync()
        {
            this.shutdownvm = await this.db.GetPrimaryReplica();

            this.ChangeDiskState(this.shutdownvm, "immutable");

        }

        private void ChangeDiskState(string vm, string state)
        {
            this.vbox.ControlVM(vm, "poweroff");
            this.vbox.ModifyHD(vm, state);
            this.vbox.StartVM(vm);
        }
    }
}
