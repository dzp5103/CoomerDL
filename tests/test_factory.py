"""
Unit tests for DownloaderFactory.
"""
import pytest
from downloader.base import BaseDownloader, DownloadResult
from downloader.factory import DownloaderFactory


class DummyDownloader(BaseDownloader):
    """Dummy downloader for testing factory."""
    
    def supports_url(self, url: str) -> bool:
        """Supports URLs containing 'dummy'."""
        return 'dummy' in url.lower()
    
    def get_site_name(self) -> str:
        """Returns test site name."""
        return "DummySite"
    
    def download(self, url: str) -> DownloadResult:
        """Mock download."""
        return DownloadResult(success=True, total_files=0, completed_files=0)


class AnotherDummyDownloader(BaseDownloader):
    """Another dummy downloader for testing."""
    
    def supports_url(self, url: str) -> bool:
        """Supports URLs containing 'another'."""
        return 'another' in url.lower()
    
    def get_site_name(self) -> str:
        """Returns test site name."""
        return "AnotherSite"
    
    def download(self, url: str) -> DownloadResult:
        """Mock download."""
        return DownloadResult(success=True, total_files=0, completed_files=0)


@pytest.fixture(autouse=True)
def clear_factory_registry():
    """Clear factory registry before and after each test."""
    DownloaderFactory.clear_registry()
    yield
    DownloaderFactory.clear_registry()


class TestDownloaderFactoryRegistration:
    """Test downloader registration in factory."""
    
    def test_register_single_downloader(self):
        """Test registering a single downloader."""
        DownloaderFactory.register(DummyDownloader)
        
        sites = DownloaderFactory.get_supported_sites()
        assert len(sites) == 1
        assert "DummySite" in sites
    
    def test_register_multiple_downloaders(self):
        """Test registering multiple downloaders."""
        DownloaderFactory.register(DummyDownloader)
        DownloaderFactory.register(AnotherDummyDownloader)
        
        sites = DownloaderFactory.get_supported_sites()
        assert len(sites) == 2
        assert "DummySite" in sites
        assert "AnotherSite" in sites
    
    def test_register_same_downloader_twice(self):
        """Test that registering same downloader twice doesn't duplicate."""
        DownloaderFactory.register(DummyDownloader)
        DownloaderFactory.register(DummyDownloader)
        
        sites = DownloaderFactory.get_supported_sites()
        assert len(sites) == 1
    
    def test_register_as_decorator(self):
        """Test using register as a decorator."""
        @DownloaderFactory.register
        class DecoratedDownloader(BaseDownloader):
            def supports_url(self, url: str) -> bool:
                return 'decorated' in url
            
            def get_site_name(self) -> str:
                return "DecoratedSite"
            
            def download(self, url: str) -> DownloadResult:
                return DownloadResult(success=True, total_files=0, completed_files=0)
        
        sites = DownloaderFactory.get_supported_sites()
        assert "DecoratedSite" in sites
    
    def test_clear_registry(self):
        """Test clearing the registry."""
        DownloaderFactory.register(DummyDownloader)
        assert len(DownloaderFactory.get_supported_sites()) == 1
        
        DownloaderFactory.clear_registry()
        assert len(DownloaderFactory.get_supported_sites()) == 0


class TestDownloaderFactorySelection:
    """Test downloader selection by URL."""
    
    def test_get_downloader_matching_url(self, download_folder):
        """Test getting downloader for matching URL."""
        DownloaderFactory.register(DummyDownloader)
        
        downloader = DownloaderFactory.get_downloader(
            url="https://dummy.com/test",
            download_folder=download_folder
        )
        
        assert downloader is not None
        assert isinstance(downloader, DummyDownloader)
        assert downloader.download_folder == download_folder
    
    def test_get_downloader_no_match(self, download_folder):
        """Test that no downloader is returned for unsupported URL."""
        DownloaderFactory.register(DummyDownloader)
        
        downloader = DownloaderFactory.get_downloader(
            url="https://unsupported.com/test",
            download_folder=download_folder
        )
        
        assert downloader is None
    
    def test_get_downloader_first_match(self, download_folder):
        """Test that first matching downloader is returned."""
        # Register downloaders in specific order
        DownloaderFactory.register(DummyDownloader)
        DownloaderFactory.register(AnotherDummyDownloader)
        
        # Test URL that matches first downloader
        downloader = DownloaderFactory.get_downloader(
            url="https://dummy.com/test",
            download_folder=download_folder
        )
        
        assert isinstance(downloader, DummyDownloader)
        
        # Test URL that matches second downloader
        downloader2 = DownloaderFactory.get_downloader(
            url="https://another.com/test",
            download_folder=download_folder
        )
        
        assert isinstance(downloader2, AnotherDummyDownloader)
    
    def test_get_downloader_with_options(self, download_folder, download_options):
        """Test getting downloader with custom options."""
        DownloaderFactory.register(DummyDownloader)
        
        downloader = DownloaderFactory.get_downloader(
            url="https://dummy.com/test",
            download_folder=download_folder,
            options=download_options
        )
        
        assert downloader is not None
        assert downloader.options == download_options
    
    def test_get_downloader_with_callbacks(self, download_folder):
        """Test getting downloader with callbacks."""
        log_messages = []
        
        def log_callback(msg):
            log_messages.append(msg)
        
        DownloaderFactory.register(DummyDownloader)
        
        downloader = DownloaderFactory.get_downloader(
            url="https://dummy.com/test",
            download_folder=download_folder,
            log_callback=log_callback
        )
        
        assert downloader is not None
        downloader.log("Test")
        assert len(log_messages) == 1


class TestDownloaderFactorySupportedSites:
    """Test getting list of supported sites."""
    
    def test_get_supported_sites_empty(self):
        """Test getting supported sites with no registered downloaders."""
        sites = DownloaderFactory.get_supported_sites()
        assert isinstance(sites, list)
        assert len(sites) == 0
    
    def test_get_supported_sites_single(self):
        """Test getting supported sites with one downloader."""
        DownloaderFactory.register(DummyDownloader)
        
        sites = DownloaderFactory.get_supported_sites()
        assert len(sites) == 1
        assert sites[0] == "DummySite"
    
    def test_get_supported_sites_multiple(self):
        """Test getting supported sites with multiple downloaders."""
        DownloaderFactory.register(DummyDownloader)
        DownloaderFactory.register(AnotherDummyDownloader)
        
        sites = DownloaderFactory.get_supported_sites()
        assert len(sites) == 2
        assert "DummySite" in sites
        assert "AnotherSite" in sites
