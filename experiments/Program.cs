using System;
using System.Reflection;
using MongoDB.Driver;
using MongoDBExperiments.Config;
using MongoDBExperiments.Experiment;
using MongoDBExperiments.Failures;
using MongoDBExperiments.Utils;
using Autofac;
using CommandLine;
using System.Collections.Generic;
using CommandLine.Text;
using System.Threading;
using MongoDB.Bson;
using MongoDBExperiments.Utils.Logging;
using System.Linq;
using System.IO;
using System.Collections.Concurrent;

namespace MongoDBExperiments
{
    class Program
    {
        static int Main(string[] args)
        {
            var parser = new Parser(cfg =>
            {
                cfg.CaseInsensitiveEnumValues = true;
            });

            var result = parser.ParseArguments<Options>(args);
            
            if (args.Length == 1 && (args[0] == "-h" || args[0] == "--help"))
            {
                var help = HelpText.AutoBuild(result, null, null);
                Console.Error.WriteLine(help);
                return 0;
            }
            Options opts = null;
            result
                .WithParsed((options) => opts = options)
                .WithNotParsed(PrintErrors);
            
            if (opts != null)
            {
                SetupExperiment(opts);
            }

            return 0;
        }

        private static void PrintErrors(IEnumerable<Error> errors)
        {
            foreach (var err in errors)
            {
                Console.Error.WriteLine(err);
            }
        }

        private static void SetupExperiment(Options options)
        {
            //Register services
            var builder = new ContainerBuilder();

            builder
                .RegisterAssemblyTypes(AppDomain.CurrentDomain.GetAssemblies())
                .Where(t => t.GetCustomAttribute<InjectableAttribute>() != null)
                .AsSelf();

            var config = new ConfigManager(options);
            builder.RegisterType(config.GetFailureType()).As<IFailure>();

            // Set up DB connection
            var client = new MongoClient(config.GetMongoClientSettings());
            builder.RegisterInstance(client).AsSelf();

            var db = client.GetDatabase(options.Database);
            builder.RegisterInstance(db).As<IMongoDatabase>();

            var collection = db.GetCollection<ExperimentDocument>(options.Collection);
            builder.RegisterInstance(collection).As<IMongoCollection<ExperimentDocument>>();

            var servers = config.GetServers();
            var instanceIds = config.GetInstanceIds();
            IDictionary<string, string> ec2InstanceId = new Dictionary<string, string>();
            foreach(var serversAndInstanceIds in servers.Zip(instanceIds, Tuple.Create))
            {
                ec2InstanceId.Add(serversAndInstanceIds.Item1.ToString(), serversAndInstanceIds.Item2);
            }
            Console.WriteLine(ec2InstanceId.ToString());
            builder.RegisterInstance(ec2InstanceId).As<IDictionary<string, string>>();

            var container = builder.Build();

            Console.Error.WriteLine
            ($@"
                Failure: {options.Failure}
                Read Pref: {options.ReadPreference}
                Read Concern: {options.ReadConcern}
                Write Concern: {options.WriteConcern}
            ");

            Warmup(client);

            Console.Error.WriteLine("Warmup complete. Setting up...");

            Thread[] runners = new Thread[options.NumThreads + 1];
            ConcurrentBag<IEnumerable<ILogRecord>> logs = new ConcurrentBag<IEnumerable<ILogRecord>>();

            for (var i = 0; i < options.NumThreads; i++)
            {
                var runner = container.Resolve<ExperimentRunner>();
                runners[i] = new Thread(() => logs.Add(runner.Run(options.OperationInterval, options.IntervalVariance, options.WriteProbability, options.ExperimentTime)));
            }

            var fail = container.Resolve<FailureRunner>();
            (DateTime fail, DateTime fix) stages = (DateTime.Now, DateTime.Now);
            runners[options.NumThreads] = new Thread( () => stages = fail.Run(options.ExperimentTime));

            for (var i = 0; i <= options.NumThreads; i++)
            {
                runners[i].Start();
            }
            Console.Error.WriteLine("Started experiment");

            for (var i = 0; i <= options.NumThreads; i++)
            {
                runners[i].Join();
            }
            Console.Error.WriteLine("Threads finished");

            var completeLogs = new List<ILogRecord>();
            foreach (var l in logs)
                completeLogs.AddRange(l);

            Console.Error.WriteLine($"Ordering and writing {completeLogs.Count()} records");
            completeLogs = completeLogs.OrderBy(r => r.TimeStamp.ToUnixTimeStamp()).ToList();

            Console.WriteLine($"{stages.fail.ToUnixTimeStamp()},{stages.fix.ToUnixTimeStamp()}");
            foreach (var t in completeLogs)
            {
                Console.WriteLine(t.ToString());
            }

        }

        public static void Warmup(MongoClient client)
        {
            while (true)
            {
                var status = client.GetDatabase("admin").RunCommand<BsonDocument>(new BsonDocument("replSetGetStatus", 1));
                if (status["ok"] == 1)
                {
                    break;
                }

                Thread.Sleep(100);
            }
        }
    }
}
