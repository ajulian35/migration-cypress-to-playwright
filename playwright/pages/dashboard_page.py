from playwright.sync_api import Page
from .base_page import BasePage

class DashboardPage(BasePage):
    URL = "/web/index.php/dashboard/index"

    HEADING = 'h6.oxd-topbar-header-breadcrumb-module'

    def is_loaded(self):
        self.page.wait_for_url("**/dashboard/index", timeout=60000)
        assert "dashboard/index" in self.page.url
        assert self.page.text_content(self.HEADING) == "Dashboard"
