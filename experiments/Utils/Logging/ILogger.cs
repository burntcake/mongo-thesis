using System;
using System.Collections.Generic;

namespace MongoDBExperiments.Utils.Logging
{
    public interface ILogger
    {
        IEnumerable<ILogRecord> GetLogs();
    }
}
