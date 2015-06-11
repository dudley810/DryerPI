using Microsoft.AspNet.SignalR;
using SignalrServer.Hubs.RealTimeHub;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;

namespace SignalrServer.Controllers
{
    public class StopPiController : ApiController
    {
        public HttpResponseMessage PostStop()
        {
            try
            {
                GlobalHost.ConnectionManager.GetHubContext<RealTimeHub>().Clients.All.SendMessage("PI Has Stopped");
                Common.SendEmail("PI","THE PI IS NOW SHUTTING DOWN",false);
                return Request.CreateResponse(HttpStatusCode.OK, "THE PI IS NOW SHUTTING DOWN");
            }
            catch (Exception ex)
            {
                GlobalHost.ConnectionManager.GetHubContext<RealTimeHub>().Clients.All.SendMessage("Dryer email code had an issue:" + ex.Message);
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, ex.Message);
            }
        }


    }
}
