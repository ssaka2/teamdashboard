using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Student.Controllers;

[Area("Student")]
public class HomeController : Controller
{
    public ContentResult Index() => Content("Student Area - Home Controller - Index Action", "text/plain");
}
