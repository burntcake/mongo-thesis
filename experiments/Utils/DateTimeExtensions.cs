using System;
namespace MongoDBExperiments.Utils
{
    public static class DateTimeExtensions
    {
        public static long ToUnixTimeStamp(this DateTime time)
        {
            return new DateTimeOffset(time).ToUnixTimeMilliseconds();
        }
    }
}
