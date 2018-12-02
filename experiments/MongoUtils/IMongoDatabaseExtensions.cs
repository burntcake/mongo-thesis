using System;
using System.Threading.Tasks;
using MongoDB.Bson;
using MongoDB.Driver;

namespace MongoDBExperiments.MongoUtils
{
    public static class IMongoDatabaseExtensions
    {
        public static string GetPrimaryReplica(this IMongoDatabase db)
        {
            var result = db.RunCommand<BsonDocument>(new BsonDocument("isMaster", 1));
            var primary = result["primary"].AsString;

            return primary.Split(':')[0];
        }
    }
}
