using Microsoft.AspNetCore.Mvc;

namespace Group3Blackboard.Areas.Student.Controllers;

[Area("Student")]
public class CatalogController : Controller
{
    public ContentResult Index() => Content("Student Area - Catalog Controller - Index Action", "text/plain");
}
