import json
import inquirer
from colorama import init, Fore, Style
import requests
from bs4 import BeautifulSoup
import os

init()

class ConfigGenerator:
    def __init__(self):
        self.config = {
            "name": "",
            "base_url": "",
            "login_path": "",
            "search_path": "",
            "selectors": {
                "email_input": "",
                "password_input": "",
                "submit_button": "",
                "cookie_consent": "",
                "target_elements": [],
                "next_page": ""
            },
            "delays": {
                "page_load": 5,
                "between_requests": 2,
                "after_login": 4
            },
            "pagination": {
                "type_": "",
                "param_name": None,
                "path_format": None
            }
        }

    def generate(self):
        print(f"{Fore.CYAN}=== Web Scraper Configuration Generator ==={Style.RESET_ALL}")
        
        # Basic information
        questions = [
            inquirer.Text('name', message="Enter configuration name"),
            inquirer.Text('base_url', message="Enter base URL (e.g., https://example.com)"),
            inquirer.Text('login_path', message="Enter login path (e.g., /login)"),
            inquirer.Text('search_path', message="Enter search path (e.g., /search)"),
        ]
        answers = inquirer.prompt(questions)
        self.config.update(answers)
        
        # Selectors
        print(f"\n{Fore.YELLOW}Enter CSS selectors:{Style.RESET_ALL}")
        selector_questions = [
            inquirer.Text('email_input', message="Email input selector"),
            inquirer.Text('password_input', message="Password input selector"),
            inquirer.Text('submit_button', message="Submit button selector"),
            inquirer.Text('cookie_consent', message="Cookie consent button selector (optional)"),
            inquirer.Text('next_page', message="Next page button/link selector"),
        ]
        answers = inquirer.prompt(selector_questions)
        self.config["selectors"].update(answers)
        
        # Target elements
        while True:
            if not inquirer.confirm("Add target element selector?", default=True):
                break
            selector = inquirer.text("Enter target element selector")
            self.config["selectors"]["target_elements"].append(selector)
        
        # Delays
        print(f"\n{Fore.YELLOW}Configure delays (in seconds):{Style.RESET_ALL}")
        delay_questions = [
            inquirer.Text('page_load', message="Page load delay", default="5"),
            inquirer.Text('between_requests', message="Delay between requests", default="2"),
            inquirer.Text('after_login', message="Delay after login", default="4"),
        ]
        answers = inquirer.prompt(delay_questions)
        self.config["delays"].update({k: int(v) for k, v in answers.items()})
        
        # Pagination
        pagination_type = inquirer.list_input(
            "Select pagination type",
            choices=["query_param", "path"]
        )
        self.config["pagination"]["type_"] = pagination_type
        
        if pagination_type == "query_param":
            param_name = inquirer.text("Enter page parameter name (e.g., page)")
            self.config["pagination"]["param_name"] = param_name
        else:
            path_format = inquirer.text(
                "Enter path format (use {page} and {query} placeholders)"
            )
            self.config["pagination"]["path_format"] = path_format
        
        # Save configuration
        filename = inquirer.text("Enter filename to save configuration", default="scraper_config.json")
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        print(f"\n{Fore.GREEN}Configuration saved to {filename}{Style.RESET_ALL}")

if __name__ == "__main__":
    generator = ConfigGenerator()
    generator.generate()
