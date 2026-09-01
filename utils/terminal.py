"""Terminal output helpers with consistent formatting and colors.

Provides functions for displaying colored terminal output with a consistent
style throughout the application.
"""

from colorama import Fore, Style, init
from datetime import datetime
from config import BOT_NAME, BOT_FULL_NAME, VERSION

# Initialize colorama (auto-reset after each print)
init(autoreset=True)


def print_banner() -> None:
    """Print the TITAN startup banner."""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
████████ ██ ████████  █████  ██ 
   ██    ██    ██    ██   ██ ██ 
   ██    ██    ██    ███████ ██ 
   ██    ██    ██    ██   ██ ██ 
   ██    ██    ██    ██   ██ ██ 
{Style.RESET_ALL}
{Fore.CYAN}{BOT_FULL_NAME}{Fore.RESET}
{Fore.CYAN}Version {VERSION} | Official bot account only{Fore.RESET}
"""
    print(banner)


def print_section(title: str) -> None:
    """Print a section header.
    
    Args:
        title: The section title to display.
    """
    print(f"{Fore.MAGENTA}{'=' * 60}{Fore.RESET}")
    print(f"{Fore.MAGENTA}▸ {title}{Fore.RESET}")
    print(f"{Fore.MAGENTA}{'=' * 60}{Fore.RESET}")


def print_info(message: str) -> None:
    """Print an informational message.
    
    Args:
        message: The message to display.
    """
    print(f"{Fore.CYAN}ℹ {message}{Fore.RESET}")


def print_success(message: str) -> None:
    """Print a success message.
    
    Args:
        message: The message to display.
    """
    print(f"{Fore.GREEN}✓ {message}{Fore.RESET}")


def print_warning(message: str) -> None:
    """Print a warning message.
    
    Args:
        message: The message to display.
    """
    print(f"{Fore.YELLOW}⚠ {message}{Fore.RESET}")


def print_error(message: str) -> None:
    """Print an error message.
    
    Args:
        message: The message to display.
    """
    print(f"{Fore.RED}✗ {message}{Fore.RESET}")


def print_timestamp(message: str) -> None:
    """Print a message with timestamp.
    
    Args:
        message: The message to display.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}{Style.DIM}[{timestamp}]{Style.RESET_ALL} {message}")
