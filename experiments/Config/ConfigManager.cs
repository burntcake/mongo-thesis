using System;
using System.Collections.Generic;
using MongoDB.Driver;
using MongoDBExperiments.Failures;
using MongoDB.Driver.Core;

namespace MongoDBExperiments.Config
{
    public class ConfigManager
    {
        private readonly Options opts;

        public ConfigManager(Options opts)
        {
            this.opts = opts;
        }

        public Type GetFailureType()
        {
            switch (this.opts.Failure)
            {
                case Failure.ShutDown:
                    return typeof(ShutDownFailure);
                case Failure.PowerOff:
                    return typeof(PowerOffFailure);
                case Failure.NoFailure:
                    return typeof(NoFailure);
                //case Failure.EatMyData:
                    //return typeof(EatMyDataFailure);
                
            }
            throw new Exception("Failure unrecognised");
        }

        public MongoClientSettings GetMongoClientSettings()
        {
            return new MongoClientSettings
            {
                ReadConcern = GetReadConcern(),
                ReadPreference = GetReadPreference(),
                WriteConcern = GetWriteConcern(),
                Servers = GetServers(),
                ReplicaSetName = opts.ReplicaSet,
                MaxConnectionPoolSize = this.opts.NumThreads,
                MinConnectionPoolSize = this.opts.NumThreads,
                SocketTimeout = TimeSpan.FromSeconds(5)
            };
        }

        public IEnumerable<MongoServerAddress> GetServers()
        {
            foreach (var s in this.opts.Servers)
            {
                yield return new MongoServerAddress(s);
            }
        }

        private MongoDB.Driver.WriteConcern GetWriteConcern()
        {
            switch (this.opts.WriteConcern)
            {
                case WriteConcern.Primary:
                    return new MongoDB.Driver.WriteConcern(w: 1, journal: false);
                case WriteConcern.Journaled:
                    return new MongoDB.Driver.WriteConcern(w: 1, journal: true);
                case WriteConcern.Majority:
                    return new MongoDB.Driver.WriteConcern(mode: "majority", journal: true);
            }
            throw new Exception("Write concern wrong");
        }

        private MongoDB.Driver.ReadPreference GetReadPreference()
        {
            switch (this.opts.ReadPreference)
            {
                case ReadPreference.Primary:
                    return MongoDB.Driver.ReadPreference.Primary;
                case ReadPreference.PrimaryPreferred:
                    return MongoDB.Driver.ReadPreference.PrimaryPreferred;
                case ReadPreference.Secondary:
                    return MongoDB.Driver.ReadPreference.Secondary;
                case ReadPreference.SecondaryPreferred:
                    return MongoDB.Driver.ReadPreference.SecondaryPreferred;
            }
            throw new Exception("Read preference wrong");
        }

        private MongoDB.Driver.ReadConcern GetReadConcern()
        {
            switch (this.opts.ReadConcern)
            {
                case ReadConcern.Local:
                    return MongoDB.Driver.ReadConcern.Local;
                case ReadConcern.Majority:
                    return MongoDB.Driver.ReadConcern.Majority;
                case ReadConcern.Linerizable:
                    return MongoDB.Driver.ReadConcern.Linearizable;
            }
            throw new Exception("Read Concern wrong");
        }
    }
}
