import re
import requests
import logging
from ..Config import config  # Ensure this is correctly set up to import your configuration

logger = logging.getLogger(__name__)

class GitHubAgent:
    @staticmethod
    def retrieve_github_docs(link):
        try:
            pattern = r"https?://github\.com/([^/]+)/([^/]+)"
            match = re.match(pattern, link)
            if not match:
                return "Invalid GitHub URL.", None
            
            owner, repo = match.groups()
            url = f'https://api.github.com/repos/{owner}/{repo}'
            headers = {'Authorization': f'token {config.GITHUB_API_KEY}'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            data = response.json()
            summary = {
                "name": data.get("name", "No name provided"),
                "owner": data["owner"]["login"],
                "description": data.get("description", "No description provided."),
                "language": data.get("language", "Not specified"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("subscribers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "last_updated": data.get("updated_at", "No update time provided"),
                "license": data["license"]["name"] if data.get("license") else "No license",
                "clone_url": data.get("clone_url", "No clone URL provided"),
                "html_url": data.get("html_url", "No HTML URL provided"),
                "homepage": data.get("homepage", "No homepage provided"),
                "size": data.get("size", "No size information"),
                "created_at": data.get("created_at", "No creation time provided"),
                "pushed_at": data.get("pushed_at", "No push time provided"),
                "default_branch": data.get("default_branch", "No default branch provided"),
            }
            return "Scanning GitHub repository successful.", summary
        except requests.RequestException as e:
            logger.error(f"GitHub API Error: {e}")
            return f"GitHub API Error: {e}", None
        except KeyError as e:
            logger.error(f"KeyError: {e}. Please check if the required data fields are available.")
            return f"KeyError: {e}. Please check if the required data fields are available.", None
        except Exception as e:
            logger.error(f"An error occurred while scanning GitHub repository: {e}")
            return f"An error occurred while scanning GitHub repository: {e}", None
        
    @staticmethod
    def retrieve_repository_contents(link):
        try:
            pattern = r"https?://github\.com/([^/]+)/([^/]+)"
            match = re.match(pattern, link)
            if not match:
                return "Invalid GitHub URL.", None
            
            owner, repo = match.groups()            
            url = f'https://api.github.com/repos/{owner}/{repo}/contents'
            headers = {'Authorization': f'token {config.GITHUB_API_KEY}'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            contents = response.json()
            return "Scanning GitHub repository successful.", contents
        except requests.RequestException as e:
            logger.error(f"GitHub API Error: {e}")
            return f"GitHub API Error: {e}", None
        except Exception as e:
            logger.error(f"An error occurred while scanning GitHub repository: {e}")
            return f"An error occurred while scanning GitHub repository: {e}", None
        
    @staticmethod
    def view_repository_contents(link):
        try:
            pattern = r"https?://github\.com/([^/]+)/([^/]+)"
            match = re.match(pattern, link)
            if not match:
                return "Invalid GitHub URL.", None
            
            owner, repo = match.groups()            
            url = f'https://api.github.com/repos/{owner}/{repo}/contents'
            headers = {'Authorization': f'token {config.GITHUB_API_KEY}'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            contents = response.json()
            for item in contents:
                if item['type'] == 'file':
                    print(f"File: {item['name']}")
                    print(f"URL: {item['html_url']}")
                    print(f"Content:\n{item['content']}\n")
                elif item['type'] == 'dir':
                    print(f"Directory: {item['name']}")
                    print(f"URL: {item['html_url']}\n")
        except Exception as e:
            logger.error(f"An error occurred while viewing repository contents: {e}")
            print(f"An error occurred while viewing repository contents: {e}")
    
    @staticmethod
    def view_directory_contents(link):
        try:
            pattern = r"https?://github\.com/([^/]+)/([^/]+)"
            match = re.match(pattern, link)
            if not match:
                return "Invalid GitHub URL.", None
            
            owner, repo = match.groups()            
            url = f'https://api.github.com/repos/{owner}/{repo}/contents'
            headers = {'Authorization': f'token {config.GITHUB_API_KEY}'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            contents = response.json()
            for item in contents:
                if item['type'] == 'file':
                    print(f"File: {item['name']}")
                    print(f"URL: {item['html_url']}\n")
                elif item['type'] == 'dir':
                    print(f"Directory: {item['name']}")
                    print(f"URL: {item['html_url']}\n")
        except Exception as e:
            logger.error(f"An error occurred while viewing directory contents: {e}")
            print(f"An error occurred while viewing directory contents: {e}")
