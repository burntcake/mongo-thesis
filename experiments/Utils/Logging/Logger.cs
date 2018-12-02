using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace MongoDBExperiments.Utils.Logging
{
    [Injectable]
    public class Logger : ILogger
    {
        readonly LinkedList<ILogRecord> logs;

        public Logger()
        {
            this.logs = new LinkedList<ILogRecord>();
        }

        public void LogReadAsync(string id, int val, TimeSpan time)
        {
            logs.AddLast(new LogRecord("R", id, val, DateTime.Now, time));
        }

        public void LogUpdateAsync(string id, int val, TimeSpan time)
        {
            logs.AddLast(new LogRecord("U", id, val, DateTime.Now, time));
        }

        public void LogWriteAsync(string id, int val, TimeSpan time)
        {
            logs.AddLast(new LogRecord("W", id, val, DateTime.Now, time));
        }

        public void LogErrAsync(string op, string id, int val, TimeSpan time)
        {
            logs.AddLast(new LogRecord(op, id, val, DateTime.Now, time, true));
        }

        public IEnumerable<ILogRecord> GetLogs()
        {
            return this.logs;
        }
    }
}
