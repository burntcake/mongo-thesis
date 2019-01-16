using System;
using MongoDB.Driver;
using System.Threading.Tasks;

namespace MongoDBConnection
{
    class MainClass
    {
        public static void Main(string[] args)
        {
            var client = establishConnection();
            showDBs(client);
        }


        private static MongoClient establishConnection()
        {
            string username = "dawei";
            string password = "pwd2019";
            var connectionString = "mongodb://{0}:{1}@" +
                "mongodbcluster-shard-00-00-faz9v.mongodb.net:27017," +
                "mongodbcluster-shard-00-01-faz9v.mongodb.net:27017," +
                "mongodbcluster-shard-00-02-faz9v.mongodb.net:27017" +
                "/test?ssl=true&replicaSet=MongoDBCluster-shard-0&authSource=admin&retryWrites=true";
            connectionString = String.Format(connectionString, username, password);
            MongoClient dbClient = null;
            try
            {
                Console.WriteLine(connectionString); 
                dbClient = new MongoClient(connectionString);
            } 
            catch (MongoConfigurationException)
            {
                Console.WriteLine("Invalid connection string");
            }

            return dbClient;
        }

        private static void showDBs(MongoClient client)
        {
            //Database List 
            if (client == null)
            {
                Console.WriteLine("No connection is established.");
                return;
            }
            var dbList = client.ListDatabases().ToList();
            Console.WriteLine("\nThe list of databases are :");
            foreach (var item in dbList)
            {
                Console.WriteLine(item);
            }
        }
    }
}
