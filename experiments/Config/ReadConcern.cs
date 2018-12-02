using System;
namespace MongoDBExperiments.Config
{
    public enum ReadConcern
    {
        Local,
        Majority,
        Linerizable
    }
}
