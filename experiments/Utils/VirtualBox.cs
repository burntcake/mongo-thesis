using System;
using System.Diagnostics;

namespace MongoDBExperiments.Utils
{
    [Injectable]
    public class VirtualBox
    {
        private readonly CommandRunner runner;

        public VirtualBox(CommandRunner runner)
        {
            this.runner = runner;
        }

        public void ControlVM(string vm, string cmd)
        {
            runner.Run("VBoxManage", $"controlvm {vm} {cmd}");
        }

        public void StartVM(string vm)
        {
            runner.Run("VBoxManage", $"startvm {vm} --type headless");
        }

        internal void ModifyHD(string vm, string state)
        {
            runner.Run("VBoxManage", $"modifyhd --type {state} '~/VirtualBox VMs/{vm}/{vm}.vdi'");
        }
    }
}
