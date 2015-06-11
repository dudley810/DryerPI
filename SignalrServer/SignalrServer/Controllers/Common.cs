using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Net;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;

namespace SignalrServer.Controllers
{
    public class Common
    {
        public static void SendEmail(string subject,string body,bool sendtopeggy = true)
        {
            MailMessage mm = new MailMessage();
            mm.From = new MailAddress("YOURSENDEREMAILHERE@gmail.com");
            mm.To.Add("YOUREMAILHERE@gmail.com or cell phone");
            if (!Convert.ToBoolean(ConfigurationManager.AppSettings["testing"]) && sendtopeggy)
            {
                mm.To.Add("YOUREMAILHERE@gmail.com or cell phonet");
            }

            mm.Subject = subject;
            mm.Body = body;
            SmtpClient smtp = new SmtpClient("smtp.gmail.com", 587);
            smtp.EnableSsl = true;
            smtp.UseDefaultCredentials = false;
            smtp.Credentials = new NetworkCredential("YOURSENDEREMAILHERE@gmail.com", "YOURSENDERPASSWORD");
            smtp.Send(mm);
        }
    }
}
