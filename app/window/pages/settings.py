import customtkinter as ctk
from tkinter import messagebox

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.tr = app.tr
        self.settings_helper = app.settings_helper

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(header, text=self.tr("Settings"), font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        # Advanced Mode Toggle
        self.adv_var = ctk.BooleanVar(value=self.app.advanced_mode)
        self.adv_switch = ctk.CTkSwitch(
            header,
            text=self.tr("Enable Advanced Settings"),
            variable=self.adv_var,
            command=self.toggle_advanced_mode
        )
        self.adv_switch.pack(side="right")

        # Tab View
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        # Create Tabs
        self.tabs = {}
        self.tab_names = [
            ("General", self.settings_helper.render_general_tab, False),
            ("Downloads", self.settings_helper.render_downloads_tab, False),
            ("Structure", self.settings_helper.render_structure_tab, False),
            ("Universal", self.settings_helper.render_universal_tab, False),
            ("Database", self.settings_helper.render_db_tab, False),
            ("Cookies", self.settings_helper.render_cookies_tab, True),
            ("Scraper", self.settings_helper.render_scraper_tab, True),
            ("Network", self.settings_helper.render_network_tab, True),
            ("Filters", self.settings_helper.render_filters_tab, True),
            ("Logging", self.settings_helper.render_logging_tab, True)
        ]

        self.refresh_tabs()

    def refresh_tabs(self):
        # We can't easily remove tabs in CTkTabview without destroying them usually,
        # but delete works.
        # However, re-rendering might be expensive or state-losing.
        # A better way: Check which tabs should be present vs are present.

        should_show = []
        for name, render_func, is_advanced in self.tab_names:
            if not is_advanced or self.app.advanced_mode:
                should_show.append(name)

        # Remove tabs not needed
        current_tabs = list(self.tabs.keys())
        for name in current_tabs:
            if name not in should_show:
                self.tabview.delete(name)
                del self.tabs[name]

        # Add tabs needed
        for name, render_func, is_advanced in self.tab_names:
            if (not is_advanced or self.app.advanced_mode) and name not in self.tabs:
                tab = self.tabview.add(name)
                self.tabs[name] = tab
                # Render content
                try:
                    render_func(tab)
                except Exception as e:
                    ctk.CTkLabel(tab, text=f"Error loading tab: {e}").pack()

    def toggle_advanced_mode(self):
        self.app.advanced_mode = self.adv_var.get()
        self.app.settings['advanced_mode'] = self.app.advanced_mode
        self.settings_helper.save_settings()

        self.refresh_tabs()

        # Notify other pages if possible (Home Page expander visibility)
        # We can force refresh if we had a reference, or they check on focus.
        # Ideally SidebarApp has a refresh method or event.
        # For now, Home Page checks app.advanced_mode in its __init__ or manual refresh.
        # We'll trigger a UI update on the app to be safe
        self.app.update_ui_texts() # Placeholder for refresh
