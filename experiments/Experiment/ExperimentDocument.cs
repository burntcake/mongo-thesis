using System;
using MongoDB.Bson;

namespace MongoDBExperiments.Experiment
{                      
    public class ExperimentDocument
    {
        public ObjectId Id { get; set; }

        public int Val { get; set; }
    }
}
