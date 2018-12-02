using System;
using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{
    public class CorruptionFailure : IFailure
    {
        private readonly IMongoDatabase db;
        private readonly SSH ssh;

        private string corruptedVM;

        public CorruptionFailure(IMongoDatabase db, SSH ssh)
        {
            this.db = db;
            this.ssh = ssh;
        }

        public Task FixAsync()
        {
            ssh.Run(this.corruptedVM, "reboot");

            return Task.CompletedTask;
        }

        public async Task InduceAsync()
        {
            this.corruptedVM = await db.GetPrimaryReplica();
            ssh.Run(this.corruptedVM, "corrupt");
        }
    }
}
