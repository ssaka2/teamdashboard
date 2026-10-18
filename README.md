# Group3 Blackboard — Phase 1

ASP.NET Core MVC (.NET 10), with Student and Admin Areas. Uses the conventional controller/view/layout pattern and Bootstrap, as requested. No database, EF Core, or authentication is included.

## Windows + VS Code setup

1. Install the **.NET 10 SDK** and Visual Studio Code with the **C# Dev Kit** extension.
2. Extract the ZIP. In VS Code choose **File > Open Folder**, then open **Group3 Blackboard** (the folder containing `Group3Blackboard.csproj`).
3. Open **Terminal > New Terminal** and run:

   ```powershell
   dotnet --version
   dotnet restore
   dotnet build
   dotnet run --launch-profile Group3Blackboard
   ```

4. Visit **http://localhost:5073/**. You should see the Student Dashboard.
5. To stop the app, press **Ctrl+C** in the terminal. For automatic reload use `dotnet watch run --launch-profile Group3Blackboard`.

> The app also declares HTTPS port 7073. If HTTPS shows a development certificate warning, run `dotnet dev-certs https --trust` in PowerShell, then restart. You can use the HTTP URL above for simple local testing.

## Click-through checklist

| Destination | URL path | Expected result |
|---|---|---|
| Student Dashboard (default) | `/` | Blue navbar, dashboard heading, welcome text, footer |
| Student Dashboard (explicit) | `/Student/Dashboard/Index` | Same dashboard |
| Home | `/Student/Home/Index` | `Student Area - Home Controller - Index Action` |
| Catalog | `/Student/Catalog/Index` | `Student Area - Catalog Controller - Index Action` |
| Calendar | `/Student/Calendar/Index` | `Student Area - Calendar Controller - Index Action` |
| Admin Dashboard | `/Admin/Dashboard/Index` | Dark navbar, admin heading, management text, footer |
| Major | `/Admin/Majors/Index` | `Admin Area - Majors Controller - Index Action` |
| Course | `/Admin/Courses/Index` | `Admin Area - Courses Controller - Index Action` |
| Student (Admin) | `/Admin/Students/Index` | `Admin Area - Students Controller - Index Action` |

Click **Admin** on the Student Dashboard to enter the Admin Dashboard. Click **View Site** on the Admin Dashboard to return. Resize the browser narrow and use the hamburger navigation toggle to test responsiveness.

**Assignment interpretation:** The written requirement says Student navigation destinations should return `ContentResult`, including Home. Accordingly, the Student **Home** link returns plain text, while the **brand** and the root URL open the rendered Student Dashboard. This keeps the dashboard view and all required ContentResult endpoints separate. Admin navigation destinations also return plain text as required. Plain-text pages intentionally do not show the dashboard navbar; use your browser's Back button to return.

## Structure

- `Areas/Student/Controllers` — Dashboard, Home, Catalog, Calendar
- `Areas/Admin/Controllers` — Dashboard, Majors, Courses, Students
- `Areas/*/Views/Dashboard/Index.cshtml` — two dashboard Razor views
- `Views/Shared/_StudentLayout.cshtml`, `_AdminLayout.cshtml` — separate Bootstrap navbars
- `wwwroot/lib/bootstrap` — local Bootstrap 5.1.1 CSS/JS (no internet needed)
- `wwwroot/css/site.css` — small layout adjustments
- `Program.cs` — area and default routing

**Reference limitation:** The CH07c Guitar Shop source code was not included in the upload, so its exact file-by-file conventions could not be inspected. This implementation follows the standard MVC Areas, controller, Razor, and Bootstrap techniques described in the assignment.
