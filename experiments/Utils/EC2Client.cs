using System;
using System.Collections.Generic;
using System.Text;

namespace MongoDBExperiments.Utils
{   
    [Injectable]
    public class EC2Client
    {
        private readonly CommandRunner runner;
        private IDictionary<string, string> instanceIds;
        public EC2Client(CommandRunner runner, IDictionary<string, string> instanceIds)
        {
            this.runner = runner;
            this.instanceIds = instanceIds;

        }
        public void startVm(string server_ip)
        {
            string instance_id;
            if (instanceIds.TryGetValue(server_ip, out instance_id))
            {
                runner.Run("python3", $"StartStop.py ON {instance_id}");
            }
        }
        public void stopVm(string server_ip)
        {
            string instance_id;
            if (instanceIds.TryGetValue(server_ip, out instance_id))
            {
                runner.Run("python3", $"StartStop.py OFF {instance_id}");
            }
        }
        public void terminateVM(string server_ip)
        {
            string instance_id;
            if (instanceIds.TryGetValue(server_ip, out instance_id))
            {
                runner.Run("python3", $"PowerOff.py {instance_id}");
            }
        }
    }
}
