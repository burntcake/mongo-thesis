using System;
using System.Threading.Tasks;
using MongoDB.Bson;
using MongoDB.Driver;
using MongoDBExperiments.Experiment;
using MongoDBExperiments.Utils;

namespace MongoDBExperiments.MongoUtils
{
    [Injectable]
    public class MongoExperimentClient
    {
        private readonly MongoClient client;
        private readonly IMongoCollection<ExperimentDocument> collection;

        public MongoExperimentClient(MongoClient client, IMongoCollection<ExperimentDocument> collection)
        {
            this.client = client;
            this.collection = collection;
        }

        public ExperimentDocument UpdateAsync(ObjectId id, int val)
        {
            var update = Builders<ExperimentDocument>.Update.Set(d => d.Val, val);
            return collection.FindOneAndUpdate(d => d.Id == id, update);    
        }

        public void WriteAsync(ExperimentDocument doc)
        {
            collection.InsertOne(doc);
        }

        public ExperimentDocument GetAsync(ObjectId id)
        {
            var result = collection.Find(d => d.Id == id);
            return result.FirstOrDefault();
        }


    }
}
