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
    public class DryerPiController : ApiController
    {
        public HttpResponseMessage PostGPIO4Result(string GPIOResult)
        {
            try
            {
                if (GPIOResult == "0")
                {
                    GlobalHost.ConnectionManager.GetHubContext<RealTimeHub>().Clients.All.SendMessage("Dryer Complete");
                    Common.SendEmail("Dryer Complete","Your dryer is now complete!!");
                    return Request.CreateResponse(HttpStatusCode.OK, "Dryer complete email sent");
                }
                else
                {
                    return Request.CreateResponse(HttpStatusCode.OK, "Email Not Sent");
                }
            }
            catch (Exception ex)
            {
                GlobalHost.ConnectionManager.GetHubContext<RealTimeHub>().Clients.All.SendMessage("Dryer email code had an issue:" + ex.Message);
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, ex.Message);
            }
        }


    }
}
