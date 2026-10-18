using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Student.Controllers;

[Area("Student")]
public class CalendarController : Controller
{
    public ContentResult Index() => Content("Student Area - Calendar Controller - Index Action", "text/plain");
}
