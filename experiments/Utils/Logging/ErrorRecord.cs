using System;

namespace MongoDBExperiments.Utils.Logging
{
    internal class ErrorRecord : ILogRecord
    {
        public string Operation { get; private set; }

        public string Id { get; private set; }

        public DateTime TimeStamp { get; private set; }

        public int Val { get; private set; }

        public TimeSpan Duration { get; private set; }

        public ErrorRecord(string op, string id, int val, DateTime timeStamp, TimeSpan duration)
        {
            this.Operation = op;
            this.Id = id;
            this.TimeStamp = timeStamp;
            this.Val = val;
            this.Duration = duration;
        }

        public override string ToString()
        {
            return $"ERR,{this.Operation},{this.Id},{this.Val},{this.Duration.TotalMilliseconds},{this.TimeStamp.ToUnixTimeStamp()}";
        }

    }
}