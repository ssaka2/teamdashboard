using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Student.Controllers;

[Area("Student")]
public class DashboardController : Controller
{
    public IActionResult Index() => View();

    public IActionResult Error() => Content("An error occurred. Please try again.");
}
