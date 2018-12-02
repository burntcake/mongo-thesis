using System;
using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.Failures
{
    /*
	public class EatMyDataFailure : IFailure
    {
        private readonly SSH ssh;
        private readonly IMongoDatabase db;

        public EatMyDataFailure(SSH ssh, IMongoDatabase db)
        {
            this.ssh = ssh;
            this.db = db;
        }

        public Task FixAsync()
        {
            throw new NotImplementedException();
        }

        public async Task InduceAsync()
        {
            var primary = await this.db.GetPrimaryReplica();
            ssh.Run(primary, "");
        }
    }*/
}
