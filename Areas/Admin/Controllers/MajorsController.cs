using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Admin.Controllers;

[Area("Admin")]
public class MajorsController : Controller
{
    public ContentResult Index() => Content("Admin Area - Majors Controller - Index Action", "text/plain");
}
