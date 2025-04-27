#!/usr/bin/env python3

import argparse
import base64
import logging
import os
import sys
import time
from datetime import datetime
from typing import Optional

import requests
from github import Github, GithubException
from colorlog import ColoredFormatter
from stem import Signal
from stem.control import Controller

# ASCII art for hacker aesthetic
BANNER = r"""
  ____ _ _       _     _       
 / ___| (_)_ __ | |__ | |__   
| |   | | | '_ \| '_ \| '_ \  
| |___| | | |_) | | | | |_) | 
 \____|_|_|_.__/|_| |_|_.__/  
  GamikaSanjana's GitHub Profile Updater
"""

# Configure colorful logging
LOG_FORMAT = "%(log_color)s%(asctime)s [%(levelname)s] %(message)s%(reset)s"
LOG_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}
formatter = ColoredFormatter(LOG_FORMAT, log_colors=LOG_COLORS)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# File handler for logging to disk
file_handler = logging.FileHandler(f"github_updater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

class TorSession:
    """Handle Tor-based anonymous requests."""
    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }

    def renew_tor_ip(self):
        """Renew Tor circuit for a new IP."""
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                logger.info("Tor circuit renewed: New IP assigned")
        except Exception as e:
            logger.error(f"Failed to renew Tor IP: {e}")

    def get(self, url: str, *args, **kwargs) -> Optional[requests.Response]:
        """Make a GET request via Tor."""
        try:
            response = self.session.get(url, *args, **kwargs)
            response.raise_for_status()
            logger.info(f"Tor GET request to {url} succeeded: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Tor GET request to {url} failed: {e}")
            return None

class GitHubUpdater:
    """Manage GitHub profile updates."""
    def __init__(self, token: str, username: str, use_tor: bool = False):
        self.token = token
        self.username = username
        self.github = Github(token)
        self.user = self.github.get_user()
        self.tor = TorSession() if use_tor else None
        self.session = self.tor if use_tor else requests.Session()

    def update_bio(self, bio: str) -> bool:
        """Update GitHub profile bio."""
        try:
            self.user.edit(bio=bio)
            logger.info(f"Successfully updated bio to: {bio}")
            return True
        except GithubException as e:
            logger.error(f"Failed to update bio: {e}")
            return False

    def update_readme(self, repo_name: str, readme_path: str) -> bool:
        """Update README in the specified repository."""
        try:
            repo = self.github.get_repo(f"{self.username}/{repo_name}")
            with open(readme_path, 'r') as f:
                content = f.read()
            
            # Get current README
            try:
                readme = repo.get_contents("README.md")
                repo.update_file(
                    path="README.md",
                    message="Update README via CyberSmith's tool",
                    content=content,
                    sha=readme.sha
                )
            except:
                # Create new README if it doesn't exist
                repo.create_file(
                    path="README.md",
                    message="Initialize README via CyberSmith's tool",
                    content=content
                )
            
            logger.info(f"Successfully updated README in {repo_name}")
            return True
        except GithubException as e:
            logger.error(f"Failed to update README: {e}")
            return False
        except FileNotFoundError:
            logger.error(f"README file not found: {readme_path}")
            return False

    def verify_connectivity(self) -> bool:
        """Verify GitHub API connectivity."""
        url = "https://api.github.com"
        response = self.session.get(url)
        if response and response.status_code == 200:
            logger.info("GitHub API connectivity verified")
            return True
        logger.error("Failed to connect to GitHub API")
        return False

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="CyberSmith's GitHub Profile Updater",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--token",
        required=True,
        help="GitHub Personal Access Token"
    )
    parser.add_argument(
        "--username",
        required=True,
        help="GitHub username"
    )
    parser.add_argument(
        "--bio",
        help="New bio to set for the GitHub profile"
    )
    parser.add_argument(
        "--readme",
        help="Path to local README.md file to upload"
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository name for README update (default: username/username)"
    )
    parser.add_argument(
        "--tor",
        action="store_true",
        help="Use Tor for anonymous requests"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()

def main():
    """Main function to run the GitHub profile updater."""
    print(BANNER)
    args = parse_args()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Initialize updater
    logger.info("Initializing CyberSmith's GitHub Profile Updater")
    updater = GitHubUpdater(args.token, args.username, args.use_tor)

    # Verify connectivity
    if not updater.verify_connectivity():
        logger.error("Aborting due to connectivity issues")
        sys.exit(1)

    # Update bio if provided
    if args.bio:
        logger.info(f"Updating GitHub bio for {args.username}")
        if updater.update_bio(args.bio):
            print(f"[+] Bio updated successfully: {args.bio}")
        else:
            print("[-] Failed to update bio")
            sys.exit(1)

    # Update README if provided
    if args.readme:
        repo_name = args.repo or args.username
        logger.info(f"Updating README in {repo_name}")
        if updater.update_readme(repo_name, args.readme):
            print(f"[+] README updated successfully in {repo_name}")
        else:
            print("[-] Failed to update README")
            sys.exit(1)

    # Renew Tor IP if using Tor
    if args.use_tor:
        updater.tor.renew_tor_ip()

    logger.info("Operation completed. Check logs for details.")
    print("[*] Done. Stay anonymous, stay ethical.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Operation interrupted by user")
        print("\n[-] Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print("[-] An error occurred. Check logs for details.")
        sys.exit(1)
