using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Admin.Controllers;

[Area("Admin")]
public class StudentsController : Controller
{
    public ContentResult Index() => Content("Admin Area - Students Controller - Index Action", "text/plain");
}
