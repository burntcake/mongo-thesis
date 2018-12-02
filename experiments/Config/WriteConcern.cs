using System;
namespace MongoDBExperiments.Config
{
    public enum WriteConcern
    {
        Primary,
        Journaled,
        Majority
    }
}
