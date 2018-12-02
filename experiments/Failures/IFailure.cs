using System.Threading.Tasks;

namespace MongoDBExperiments.Failures
{
    public interface IFailure
    {
        void InduceAsync();

        void FixAsync();

    }
}