
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using WindowServiceInstaller;

namespace SignalrServer
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        static void Main(string[] args)
        {
            string arg0 = string.Empty;
            if (args.Length > 0)
                arg0 = (args[0] ?? string.Empty).ToLower();

            if (arg0 == "-runonserver")
            {
                RunOnServer();
                return;
            }
            else if (arg0 == "-dev")
            {
                RunOnDevMachine();
                return;
            }
            else if (arg0 == "-i")
            {
                ServiceManager SM = new ServiceManager();
                if (!SM.InstallService(Environment.CurrentDirectory + "\\" + ConfigurationManager.AppSettings["serviceexe"],
                      ConfigurationManager.AppSettings["servicename"],ConfigurationManager.AppSettings["servicedesc"]))
                {
                    //Logger.writeError("SignalrServer Service install failed.", "Program");
                }
                else
                {
                    //Logger.writeError("SignalrServer Service is now installed and ready for action.", "Program");
                }

                return;
            }
            else if (arg0 == "-u")
            {
                ServiceManager SM = new ServiceManager();
                if (!SM.UnInstallService(ConfigurationManager.AppSettings["servicename"]))
                {
                    //Logger.writeError("SignalrServer Service uninstall failed.", "Program");
                }
                else
                {
                    //Logger.writeError("SignalrServer Service is now uninstalled.", "Program");
                }
                return;
            }
        }

        static void RunOnServer()
        {
            ServiceBase[] ServicesToRun;
            ServicesToRun = new ServiceBase[] 
            { 
                new DQCSService() 
            };
            ServiceBase.Run(ServicesToRun);
        }

        static void RunOnDevMachine()
        {
            var service = new DQCSService();
            service.StartSignalrServer();
            // never ends but waits
            Console.WriteLine("The SignalrServer service is now started on localhost");
            Console.WriteLine("Press enter to end service");
            Console.ReadLine();
            service.StopSignalrServer();
        }
    }
}
