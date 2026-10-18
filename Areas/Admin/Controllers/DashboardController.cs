using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Admin.Controllers;

[Area("Admin")]
public class DashboardController : Controller
{
    public IActionResult Index() => View();
}
