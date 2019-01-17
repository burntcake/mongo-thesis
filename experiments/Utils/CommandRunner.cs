using System;
using System.Diagnostics;

namespace MongoDBExperiments.Utils
{
    [Injectable]
    public class CommandRunner
    {
        public void Run(string cmd, string args)
        {
            Console.WriteLine(cmd);
            Console.WriteLine(args);
            var proc = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = cmd,
                    Arguments = args,
                    RedirectStandardOutput = true
                }
            };

            proc.Start();
        }
    }
}
