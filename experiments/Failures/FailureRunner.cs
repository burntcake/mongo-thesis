using System;
using System.Threading;
using System.Threading.Tasks;
using MongoDBExperiments.Utils;
using MongoDBExperiments.Utils.Logging;

namespace MongoDBExperiments.Failures
{
    [Injectable]
    public class FailureRunner
    {
        private readonly IFailure failure;
        private readonly FailureLogger logger;

        public FailureRunner(IFailure failure, FailureLogger logger)
        {
            this.failure = failure;
            this.logger = logger;
        }

        public (DateTime fail, DateTime fix) Run(int experimentTime)
        {
            int time = experimentTime / 3;

            Thread.Sleep(time * 1000);

            this.failure.InduceAsync();
            Console.Error.WriteLine("Failure Induced");
            this.logger.LogFailureCompleteAsync();

            Thread.Sleep(time * 1000);

            this.failure.FixAsync();
            Console.Error.WriteLine("Failure Fixed");
            this.logger.LogFixCompleteAsync();

            return (logger.Fail, logger.Fix);
        }
    }
}
