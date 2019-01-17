using System;
using System.Collections.Generic;
using System.Text;

namespace MongoDBExperiments.Utils
{   
    [Injectable]
    public class EC2Client
    {
        private readonly CommandRunner runner;

        public EC2Client(CommandRunner runner)
        {
            this.runner = runner;
        }
        public void startVm(string instance_id)
        {
            runner.Run("python3", $"StartStop.py ON {instance_id}");
        }
        public void stopVm(string instance_id)
        {
            runner.Run("python3", $"StartStop.py OFF {instance_id}");
        }
        public void terminateVM(string instance_id)
        {
            runner.Run("python3", $"TerminateEC2Instance.py {instance_id}");
        }

    }
}
