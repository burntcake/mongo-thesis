using System;
namespace MongoDBExperiments.Utils.Logging
{
    public interface ILogRecord
    {

        string Operation { get; }

        int Val { get; }

        TimeSpan Duration { get; }

        string Id { get; }

        DateTime TimeStamp { get; }

        bool IsError { get; }

        string ToString();

    }
}
