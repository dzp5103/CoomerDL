"""
Base downloader class that all site-specific downloaders must inherit from.
Provides standardized interface and common functionality.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any
from enum import Enum
import threading
import re


class DownloadStatus(Enum):
    """Status of a download item."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


@dataclass
class DownloadOptions:
    """Configuration options for downloads."""
    download_images: bool = True
    download_videos: bool = True
    download_compressed: bool = True
    download_documents: bool = True
    max_retries: int = 3
    retry_interval: float = 2.0
    chunk_size: int = 1048576  # 1MB
    timeout: int = 30
    min_file_size: int = 0  # bytes, 0 = no minimum
    max_file_size: int = 0  # bytes, 0 = no maximum
    date_from: Optional[str] = None  # ISO format YYYY-MM-DD
    date_to: Optional[str] = None  # ISO format YYYY-MM-DD


@dataclass
class MediaItem:
    """Represents a single media file to download."""
    url: str
    filename: str
    file_type: str  # 'image', 'video', 'document', 'compressed', 'other'
    size: Optional[int] = None
    post_id: Optional[str] = None
    user_id: Optional[str] = None
    published_date: Optional[str] = None


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    total_files: int
    completed_files: int
    failed_files: List[str] = field(default_factory=list)
    skipped_files: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    total_bytes: int = 0
    elapsed_seconds: float = 0.0


class BaseDownloader(ABC):
    """
    Abstract base class for all site-specific downloaders.
    
    All downloaders must implement:
    - supports_url(url) -> bool
    - get_site_name() -> str
    - download(url) -> DownloadResult
    
    Provides common functionality:
    - Cancellation via threading.Event
    - Progress reporting via callbacks
    - Logging via callback
    - File type filtering
    """
    
    # Class-level list of supported file extensions by type
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.webm', '.mov', '.avi', '.flv', '.wmv', '.m4v'}
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'}
    COMPRESSED_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz'}
    
    def __init__(
        self,
        download_folder: str,
        options: Optional[DownloadOptions] = None,
        log_callback: Optional[Callable[[str], None]] = None,
        progress_callback: Optional[Callable[[int, int, Dict[str, Any]], None]] = None,
        global_progress_callback: Optional[Callable[[int, int], None]] = None,
        enable_widgets_callback: Optional[Callable[[bool], None]] = None,
        tr: Optional[Callable[[str], str]] = None,
    ):
        """
        Initialize the downloader.
        
        Args:
            download_folder: Path to save downloaded files
            options: Download configuration options
            log_callback: Function to call with log messages
            progress_callback: Function to call with per-file progress (downloaded, total, metadata)
            global_progress_callback: Function to call with overall progress (completed, total)
            enable_widgets_callback: Function to enable/disable UI widgets
            tr: Translation function for internationalization
        """
        self.download_folder = download_folder
        self.options = options or DownloadOptions()
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.global_progress_callback = global_progress_callback
        self.enable_widgets_callback = enable_widgets_callback
        self.tr = tr or (lambda x: x)  # Default to identity function if no translation
        
        # Cancellation mechanism - use Event for thread safety
        self.cancel_event = threading.Event()
        
        # Progress tracking
        self.total_files = 0
        self.completed_files = 0
        self.failed_files: List[str] = []
        self.skipped_files: List[str] = []
    
    @abstractmethod
    def supports_url(self, url: str) -> bool:
        """
        Check if this downloader can handle the given URL.
        
        Args:
            url: The URL to check
            
        Returns:
            True if this downloader supports the URL, False otherwise
        """
        pass
    
    @abstractmethod
    def get_site_name(self) -> str:
        """
        Get the human-readable name of the site this downloader handles.
        
        Returns:
            Site name (e.g., "Coomer", "Kemono", "Erome")
        """
        pass
    
    @abstractmethod
    def download(self, url: str) -> DownloadResult:
        """
        Download all media from the given URL.
        
        Args:
            url: The URL to download from (profile, post, or album)
            
        Returns:
            DownloadResult with statistics about the download
        """
        pass
    
    def request_cancel(self) -> None:
        """Request cancellation of the current download."""
        self.cancel_event.set()
        self.log(self.tr("Download cancellation requested."))
    
    def is_cancelled(self) -> bool:
        """Check if cancellation was requested."""
        return self.cancel_event.is_set()
    
    def reset(self) -> None:
        """Reset the downloader state for a new download."""
        self.cancel_event.clear()
        self.total_files = 0
        self.completed_files = 0
        self.failed_files = []
        self.skipped_files = []
    
    def log(self, message: str) -> None:
        """Log a message through the callback."""
        if self.log_callback:
            self.log_callback(message)
    
    def report_progress(self, downloaded: int, total: int, **kwargs) -> None:
        """Report per-file download progress."""
        if self.progress_callback:
            self.progress_callback(downloaded, total, kwargs)
    
    def report_global_progress(self) -> None:
        """Report overall download progress."""
        if self.global_progress_callback:
            self.global_progress_callback(self.completed_files, self.total_files)
    
    def enable_widgets(self, enabled: bool) -> None:
        """Enable or disable UI widgets."""
        if self.enable_widgets_callback:
            self.enable_widgets_callback(enabled)
    
    def get_file_type(self, filename: str) -> str:
        """
        Determine file type from extension.
        
        Args:
            filename: The filename to check
            
        Returns:
            One of: 'image', 'video', 'document', 'compressed', 'other'
        """
        ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        if ext in self.IMAGE_EXTENSIONS:
            return 'image'
        elif ext in self.VIDEO_EXTENSIONS:
            return 'video'
        elif ext in self.DOCUMENT_EXTENSIONS:
            return 'document'
        elif ext in self.COMPRESSED_EXTENSIONS:
            return 'compressed'
        return 'other'
    
    def should_download_file(self, media_item: MediaItem) -> bool:
        """
        Check if a file should be downloaded based on options.
        
        Args:
            media_item: The media item to check
            
        Returns:
            True if the file should be downloaded, False to skip
        """
        file_type = media_item.file_type or self.get_file_type(media_item.filename)
        
        # Check file type filters
        if file_type == 'image' and not self.options.download_images:
            return False
        if file_type == 'video' and not self.options.download_videos:
            return False
        if file_type == 'document' and not self.options.download_documents:
            return False
        if file_type == 'compressed' and not self.options.download_compressed:
            return False
        
        # Check file size filters
        if media_item.size:
            if self.options.min_file_size > 0 and media_item.size < self.options.min_file_size:
                return False
            if self.options.max_file_size > 0 and media_item.size > self.options.max_file_size:
                return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Remove invalid characters from filename.
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename safe for all platforms
        """
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
