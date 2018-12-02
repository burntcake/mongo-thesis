using System;
namespace MongoDBExperiments.Utils
{
    [Injectable]
    public class SSH
    {
        private readonly CommandRunner runner;

        public SSH(CommandRunner runner)
        {
            this.runner = runner;
        }

        public void Run(string vm, string cmd)
        {
            runner.Run("ssh", $"kosta@{vm} 'sudo {cmd}'");
        }
    }
}
