"""SimpCity downloader.

This module follows the refactored downloader architecture that uses
:class:`~downloader.base.BaseDownloader` and a registration-based factory.

It also provides backward-compatible aliases for older imports.
"""

from __future__ import annotations

from downloader.base import BaseDownloader
from downloader.factory import DownloaderFactory


@DownloaderFactory.register
class SimpCity(BaseDownloader):
    """Downloader for simpcity.su threads."""

    name = "simpcity"

    @classmethod
    def supports_url(cls, url: str) -> bool:
        # Keep the broader check from main to avoid missing alternative paths.
        return "simpcity" in (url or "").lower()


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------
# Some parts of the codebase (or external integrations) may still import the
# old class name. Keep these aliases.
SimpCityDownloader = SimpCity

# Older code may do `from downloader.simpcity import SimpCity` expecting the
# downloader class to be named SimpCity. It's already the class name here, but
# keep an explicit alias in case of future refactors.
SimpCity = SimpCity
