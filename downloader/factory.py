"""
Factory for creating downloader instances based on URL.
"""
from typing import Optional, List, Type
from downloader.base import BaseDownloader, DownloadOptions


class DownloaderFactory:
    """
    Factory class for creating appropriate downloader based on URL.
    
    Priority order:
    1. Native/specialized downloaders (Coomer, Kemono, SimpCity, etc.)
    2. yt-dlp Universal downloader (for 1000+ sites)
    3. Generic HTML scraper (last resort fallback)
    
    Usage:
        factory = DownloaderFactory()
        factory.register(CoomerDownloader)
        factory.register(EromeDownloader)
        
        downloader = factory.get_downloader(url, download_folder="/downloads")
        if downloader:
            result = downloader.download(url)
    """
    
    _downloader_classes: List[Type[BaseDownloader]] = []
    
    @classmethod
    def register(cls, downloader_class: Type[BaseDownloader]) -> Type[BaseDownloader]:
        """
        Register a downloader class. Can be used as decorator.
        
        Args:
            downloader_class: The downloader class to register
            
        Returns:
            The same class (for decorator usage)
        """
        if downloader_class not in cls._downloader_classes:
            cls._downloader_classes.append(downloader_class)
        return downloader_class
    
    @classmethod
    def get_downloader(
        cls,
        url: str,
        download_folder: str,
        options: Optional[DownloadOptions] = None,
        use_generic_fallback: bool = True,
        use_ytdlp_fallback: bool = True,
        ytdlp_options=None,
        **kwargs
    ) -> Optional[BaseDownloader]:
        """
        Get appropriate downloader for the given URL.
        
        Priority:
        1. Native downloaders (specialized, faster)
        2. yt-dlp downloader (universal, supports 1000+ sites)
        3. Generic HTML scraper (last resort)
        
        Args:
            url: The URL to find a downloader for
            download_folder: Path to save downloaded files
            options: Download configuration options
            use_generic_fallback: If True, use GenericDownloader as last resort
            use_ytdlp_fallback: If True, use YtDlpDownloader before generic fallback
            ytdlp_options: Optional YtDlpOptions for yt-dlp configuration
            **kwargs: Additional arguments passed to downloader constructor
            
        Returns:
            Appropriate downloader instance, or None if no match
        """
        # Try specific/native downloaders first (highest priority)
        for downloader_class in cls._downloader_classes:
            # Create temporary instance to check URL support
            instance = downloader_class(
                download_folder=download_folder,
                options=options,
                **kwargs
            )
            if instance.supports_url(url):
                return instance
        
        # Try yt-dlp universal downloader (second priority)
        if use_ytdlp_fallback:
            try:
                from downloader.ytdlp_adapter import YtDlpDownloader
                
                ytdlp_instance = YtDlpDownloader(
                    download_folder=download_folder,
                    options=options,
                    ytdlp_options=ytdlp_options,
                    **kwargs
                )
                if ytdlp_instance.supports_url(url):
                    return ytdlp_instance
            except ImportError:
                # yt-dlp not installed, fall through to generic
                pass
        
        # If no specific downloader found and generic fallback enabled (lowest priority)
        if use_generic_fallback:
            # Try to import and use GenericDownloader
            try:
                from downloader.generic import GenericDownloader
                return GenericDownloader(
                    download_folder=download_folder,
                    options=options,
                    **kwargs
                )
            except ImportError:
                pass
        
        return None
    
    @classmethod
    def get_supported_sites(cls) -> List[str]:
        """
        Get list of all supported site names.
        
        Returns:
            List of site names from registered downloaders
        """
        sites = []
        for downloader_class in cls._downloader_classes:
            # Create minimal instance to get site name
            instance = downloader_class(download_folder="")
            sites.append(instance.get_site_name())
        
        # Add yt-dlp universal support indicator
        try:
            from downloader.ytdlp_adapter import YtDlpDownloader
            sites.append("Universal (yt-dlp) - 1000+ sites")
        except ImportError:
            pass
        
        return sites
    
    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered downloaders (useful for testing)."""
        cls._downloader_classes = []


# Auto-import downloaders to ensure their @register decorators execute
# This is important for the factory pattern to work properly
try:
    from downloader import bunkr, erome, simpcity, generic, reddit
except ImportError:
    # Some downloaders might not be available
    pass
