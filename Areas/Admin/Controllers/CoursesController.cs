using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Admin.Controllers;

[Area("Admin")]
public class CoursesController : Controller
{
    public ContentResult Index() => Content("Admin Area - Courses Controller - Index Action", "text/plain");
}
