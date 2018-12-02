using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace MongoDBExperiments.Utils.Logging
{
    [Injectable]
    public class FailureLogger
    {
        public DateTime Fail { get; private set; }
        public DateTime Fix { get; private set; }

        public void LogFailureCompleteAsync()
        {
            this.Fail = DateTime.Now;
        }

        public void LogFixCompleteAsync()
        {
            this.Fix = DateTime.Now;
        }
    }
}
