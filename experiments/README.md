# Experiment Harness

This is the C# codebase for the experiment harness. Written in .NET Core.

The harness heavily utilises commandline arguments and outputs the execution history into `stdout`. Running `dotnet run -- -h` will show all commandline options.

The harness assumes that the virtual machines are all turned on and reachable using the names provided (default `mongo1, mongo2, mongo3`). It also assumes the machines are configured to run in a replica set. 

To run an experiment with default arguments run:

`dotnet run`
