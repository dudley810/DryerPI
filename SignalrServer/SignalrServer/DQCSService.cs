using Microsoft.Owin.Hosting;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;

namespace SignalrServer
{
    public partial class DQCSService : ServiceBase
    {
        IDisposable SignalR { get; set; }

        public DQCSService()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            StartSignalrServer();
        }

        public void StartSignalrServer()
        {
            try
            {
                SignalR = WebApp.Start<Startup>("http://*:" + ConfigurationManager.AppSettings["serviceport"] + "/");
            }
            catch 
            {

            }
        }

        protected override void OnStop()
        {
            StopSignalrServer();
        }
        public void StopSignalrServer()
        {
            try
            {
                SignalR.Dispose();
            }
            catch
            {
            }
        }
    }
}
