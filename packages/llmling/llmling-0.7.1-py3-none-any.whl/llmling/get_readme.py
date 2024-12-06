"""Functions for retrieving package information."""

from __future__ import annotations

import json
import re
from typing import Any

from upath import UPath


def autocomplete(arg):
    return ["httpx", "requests", "aiohttp", "flask", "django", "fastapi"]


def get_readme(package_name: str) -> str:
    """Get README content from a Python package's GitHub repository (sync version).

    Tries to detect the GitHub repository from PyPI metadata and fetches
    the README.md file from the repository root.

    Args:
        package_name: Name of the PyPI package

    Returns:
        Content of the README file if found

    Raises:
        ValueError: If package not found or README couldn't be retrieved
    """
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        # Get PyPI metadata
        pypi_path = UPath(pypi_url)
        try:
            data = json.loads(pypi_path.read_text())
        except Exception as exc:
            msg = f"Package {package_name} not found on PyPI"
            raise ValueError(msg) from exc

        # Try to find GitHub URLs in various metadata fields
        github_url = _extract_github_url(data["info"])
        if not github_url:
            msg = f"No GitHub repository found for package {package_name}"
            raise ValueError(msg)

        # Convert HTTPS URL to raw content URL for README
        raw_url = github_url.replace("github.com", "raw.githubusercontent.com").rstrip(
            "/"
        )

        # Try main branch first, fall back to master
        readme_path = UPath(f"{raw_url}/main/README.md")
        try:
            return readme_path.read_text()
        except Exception:
            readme_path = UPath(f"{raw_url}/master/README.md")
            try:
                return readme_path.read_text()
            except Exception as exc:
                msg = f"README not found in repository: {exc}"
                raise ValueError(msg) from exc

    except KeyError as exc:
        msg = f"Invalid PyPI metadata for package {package_name}"
        raise ValueError(msg) from exc


def _extract_github_url(info: dict[str, Any]) -> str | None:
    """Extract GitHub repository URL from PyPI package info."""
    # Common places to find GitHub URLs
    url_fields = [
        info.get("project_urls", {}).get("Source"),
        info.get("project_urls", {}).get("Homepage"),
        info.get("home_page"),
        info.get("download_url"),
    ]

    # GitHub URL pattern
    github_pattern = re.compile(
        r"https?://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+/?",
        re.IGNORECASE,
    )

    # Try each field
    for url in url_fields:
        if not url:
            continue
        if match := github_pattern.search(url):
            return match.group(0)

    return None


if __name__ == "__main__":
    # Test with a known package
    readme = get_readme("httpx")
    print(f"Found README ({len(readme)} chars)")
    print(readme[:500] + "...\n")
