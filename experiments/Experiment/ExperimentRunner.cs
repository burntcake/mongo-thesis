using System.Timers;
using System.Threading.Tasks;
using MongoDB.Driver;
using System.Collections.Concurrent;
using MongoDB.Bson;
using System;
using MongoDBExperiments.Failures;
using MongoDBExperiments.Utils;
using System.Threading;
using System.Collections.Generic;
using MongoDBExperiments.MongoUtils;
using MongoDBExperiments.Utils.Logging;

namespace MongoDBExperiments.Experiment
{
    [Injectable]
    public class ExperimentRunner
    {

        private readonly Logger logger;
        private readonly MongoExperimentClient client;

        private List<ObjectId> ids;
        private Random rng;

        public ExperimentRunner(Logger logger, MongoExperimentClient client)
        {
            this.logger = logger;
            this.client = client;
            this.rng = new Random();
            this.ids = new List<ObjectId>();
        }

        public IEnumerable<ILogRecord> Run(int opInterval, int variance, double writeLoad, int experimentTime)
        {
            Setup();

            var endTime = DateTime.Now.AddSeconds(experimentTime);

            while (DateTime.Now < endTime)
            {
                RunOpAsync(writeLoad);
            }

            return logger.GetLogs();

        }

        private void Setup()
        {
            for (int i = 0; i < 5; i++)
            {
                WriteAsync();
            }

        }

        private void RunOpAsync(double writeLoad)
        {

            if (rng.NextDouble() < writeLoad)
            {
                if (rng.NextDouble() > 0.5)
                {
                    WriteAsync();
                }
                else
                {
                    UpdateAsync();
                }
            }
            else
            {
                ReadAsync();
            }
        }

        private void ReadAsync()
        {
            var id = GetRandomObjectId();

            ExperimentDocument resultValue;

            DateTime before = DateTime.Now;

            try
            {
                resultValue = client.GetAsync(id);
            }
            catch
            {
                logger.LogErrAsync("R", id.ToString(), -1, DateTime.Now - before);
                return;
            }
            DateTime after = DateTime.Now;

            logger.LogReadAsync(id.ToString(), resultValue?.Val ?? -1, after - before);

        }

        private void WriteAsync()
        {
            int val = rng.Next();
            TimeSpan time = new TimeSpan(DateTimeOffset.UtcNow.Ticks);
            long microSeconds = (time.Ticks - ((long)time.TotalSeconds * 10000000)) / 10;
            var doc = new ExperimentDocument { Val = val , MsSinceEpoch = $"{{ts: \"{DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString()}s {microSeconds}us\"}}"};

            DateTime before = DateTime.Now;

            try
            {
                client.WriteAsync(doc);
            }
            catch
            {
                logger.LogErrAsync("W", rng.Next().ToString(), val, DateTime.Now - before);
                return;
            }

            DateTime after = DateTime.Now;
            var id = doc.Id;
            ids.Add(id);

            logger.LogWriteAsync(doc.Id.ToString(), val, after - before);
        }

        private void UpdateAsync()
        {
            var id = GetRandomObjectId();

            int val = rng.Next();

            ExperimentDocument doc;

            DateTime before = DateTime.Now;

            try
            {
                doc = client.UpdateAsync(id, val);
            }
            catch
            {
                logger.LogErrAsync("U", id.ToString(), val, DateTime.Now - before);
                return;
            }

            if (doc == null)
            {
                logger.LogErrAsync("U", id.ToString(), val, DateTime.Now - before);
                return;
            }

            DateTime after = DateTime.Now;

            logger.LogUpdateAsync(doc.Id.ToString(), val, after - before);
        }

        private ObjectId GetRandomObjectId()
        {
            int index = rng.Next(0, ids.Count);

            return ids[index];    

        }
    }
}
