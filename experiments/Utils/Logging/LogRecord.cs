using System;
namespace MongoDBExperiments.Utils.Logging
{
    public struct LogRecord : ILogRecord
    {
        public string Operation { get; private set; }

        public string Id { get; private set; }

        public DateTime TimeStamp { get; private set; }

        public int Val { get; private set; }

        public TimeSpan Duration { get; private set; }

        public bool IsError  { get; private set; }

        public LogRecord(string op, string id, int val, DateTime timeStamp, TimeSpan duration, bool isError = false)
        {
            this.Operation = op;
            this.Id = id;
            this.TimeStamp = timeStamp;
            this.Val = val;
            this.Duration = duration;
            this.IsError = isError;
        }

        public override string ToString()
        {
            var errString = this.IsError ? "ERR," : "";
            return $"{errString}{this.Operation},{this.Id},{this.Val},{this.Duration.TotalMilliseconds},{this.TimeStamp.ToUnixTimeStamp()}";
        }

    }
}
