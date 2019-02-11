using System.Collections.Generic;
using CommandLine;
namespace MongoDBExperiments.Config
{
    public class Options
    {
        
        [Option('p', "readpreference", Default = ReadPreference.Primary, HelpText = "Read preference setting for the mongo client")]
        public ReadPreference ReadPreference { get; set; }

        [Option('r', "readconcern", Default = ReadConcern.Local, HelpText = "Read concern setting for the mongo client")]
        public ReadConcern ReadConcern { get; set; }

        [Option('w', "writeconcern", Default = WriteConcern.Journaled, HelpText = "Write concern setting for the mongo client")]
        public WriteConcern WriteConcern { get; set; }

        [Option('f', "failure", Default = Failure.ShutDown, HelpText = "The type of failure to induce in this experiment")]
        public Failure Failure { get; set; }

        [Option(Default = "testCollection", HelpText = "Collection to use for this experiment")]
        public string Collection { get; set; }

        [Option(Default = "test", HelpText = "Database to use for this experiment")]
        public string Database { get; set; }

        [Option(Default = "s0", HelpText = "The Replica Set name used in the mongo servers")]
        public string ReplicaSet { get; set; }

        [Option(Default = 8)]
        public int NumThreads { get; set; }

        [Option(Default = 20, HelpText = "The interval after which another operation will be invoked (in milliseconds)")]
        public int OperationInterval { get; set; }

        [Option(Default = 10, HelpText = "The variance of the interval after which another operation is to be invoked (in milliseconds)")]
        public int IntervalVariance { get; set; }

        [Option(Default = 0.2, HelpText = "The probability that the next operation will be a write"),]
        public double WriteProbability { get; set; }

        [Option(Default = 60, HelpText = "The time this experiment will run for (in seconds)")]
        public int ExperimentTime { get; set; }

        [Option(Default = new string[] { "52.64.89.31", "52.65.140.33", "52.65.171.51" }, HelpText = "List of mongo servers")]
        public IEnumerable<string> Servers { get; set; }
        
        [Option(Default = new string[] { "i-09842854c4bcac788", "i-08fa1b3d2ed8d0068", "i-0295fa7fc6dad31fd" }, HelpText = "List of AWS instance ids. Please write in corresponding order to servers.")]
        public IEnumerable<string> InstanceIds { get; set; }
    }
}
