using System.Threading.Tasks;

namespace MongoDBExperiments.Failures
{
    public interface IFailureRunner
    {
        Task StartAsync(int experimentTime);
    }
}