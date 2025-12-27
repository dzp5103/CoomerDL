# CoomerDL Improvement Roadmap

> **Purpose**: This document outlines proposed improvements for CoomerDL to enable more features, a better UI, and a more adjustable/configurable application. This is a living document that should be refined before implementation.

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [UI/UX Improvements](#uiux-improvements)
3. [Feature Enhancements](#feature-enhancements)
4. [Architecture Improvements](#architecture-improvements)
5. [Performance Optimizations](#performance-optimizations)
6. [Configuration & Customization](#configuration--customization)
7. [Testing & Quality](#testing--quality)
8. [Implementation Priority](#implementation-priority)

---

## Current State Analysis

### Strengths
- **Multi-site support**: Supports coomer.su, kemono.su, erome.com, bunkr-albums.io, simpcity.su, jpg5.su
- **Multi-threaded downloads**: Configurable concurrent download workers
- **Progress tracking**: Real-time progress bars with speed and ETA
- **SQLite database**: Tracks downloaded files to avoid duplicates
- **Multi-language support**: 6 languages (ES, EN, JA, ZH, FR, RU)
- **Theming**: Light/Dark/System theme support via CustomTkinter
- **Cookie management**: For authenticated site access
- **Flexible file naming**: 4 different naming modes

### Current Limitations
- **Monolithic UI code**: `ui.py` is over 1200+ lines (as of December 2024), mixing concerns
- **Inconsistent downloader interfaces**: Each site downloader has different signatures
- **Limited error recovery**: Some downloaders lack robust retry mechanisms
- **No download queue management UI**: Can't pause/resume/reorder downloads
- **Missing batch URL input**: Must process URLs one at a time
- **No download history browser**: Database tab shows raw data
- **Limited filtering options**: Can't filter by date, type, or custom patterns
- **No proxy support**: Missing network configuration options
- **No bandwidth limiting**: Can saturate network connections
- **Missing scheduled downloads**: No timer/scheduler functionality

---

## UI/UX Improvements

### 1. Main Window Redesign
**Priority: High**

```
┌─────────────────────────────────────────────────────────────────┐
│  [File ▼] [Settings ▼] [Help ▼]          🌙 [Discord] [GitHub] │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ URL Input (multi-line textarea for batch URLs)            │  │
│  │ Drag & Drop zone for URL lists                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│  [📁 Select Folder] [Download Path Display]                     │
│                                                                 │
│  ┌─ Download Options ─────────────────────────────────────────┐ │
│  │ ☑ Images  ☑ Videos  ☑ Documents  ☑ Archives               │ │
│  │ [▼ Quality] [▼ Date Range] [▼ Custom Filters]             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [▶ Download] [⏸ Pause All] [⏹ Cancel All] [📋 Queue (5)]     │
│                                                                 │
│  ┌─ Active Downloads ─────────────────────────────────────────┐ │
│  │ ┌──────────────────────────────────────────────────────┐   │ │
│  │ │ 🎬 video_001.mp4    [████████░░] 78%  2.3MB/s  1:23  │   │ │
│  │ │ 🖼 image_002.jpg    [██████████] 100% Done           │   │ │
│  │ └──────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─ Logs ────────────────────────────────────────────────────┐  │
│  │ [Filter: All ▼] [Search 🔍]  [Clear] [Export]             │  │
│  │ ─────────────────────────────────────────────────────────  │  │
│  │ 12:34:56 INFO  Starting download from profile xyz...      │  │
│  │ 12:34:57 INFO  Found 45 media files                       │  │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Speed: 5.2 MB/s | ETA: 5:23 | Completed: 12/45 | Errors: 0     │
└─────────────────────────────────────────────────────────────────┘
```

**Proposed Changes:**
- [ ] Multi-line URL input for batch downloads
- [ ] Drag & drop support for URL lists (text files)
- [ ] Download queue panel with pause/resume/cancel per item
- [ ] Searchable/filterable log panel
- [ ] Enhanced status bar with more metrics
- [ ] Collapsible sections for cleaner layout
- [ ] Keyboard shortcuts (Ctrl+V paste, Ctrl+Enter download)

### 2. Settings Window Improvements
**Priority: Medium**

**Proposed Changes:**
- [ ] Reorganize into clearer categories with icons
- [ ] Add preview panels (folder structure preview already exists)
- [ ] Add profile presets (save/load settings configurations)
- [ ] Add import/export settings functionality
- [ ] Better validation and feedback for user inputs
- [ ] Reset to defaults option per section

### 3. Download Queue Manager
**Priority: High**

**New Feature:**
- [ ] Dedicated queue management window
- [ ] Drag-and-drop reordering
- [ ] Individual item controls (pause, resume, cancel, retry)
- [ ] Priority levels (high, normal, low)
- [ ] Queue persistence across app restarts
- [ ] Batch operations (select multiple, remove completed)

### 4. Download History Browser
**Priority: Medium**

**New Feature:**
- [ ] Enhanced database viewer with search/filter
- [ ] Thumbnail previews for downloaded media
- [ ] Open file/folder from history
- [ ] Re-download capability
- [ ] Statistics dashboard (total downloaded, by site, by type)
- [ ] Export history to CSV/JSON

### 5. Visual Feedback Improvements
**Priority: Medium**

**Proposed Changes:**
- [ ] Toast notifications for completed downloads
- [ ] System tray integration (minimize to tray, notifications)
- [ ] Sound notifications (optional)
- [ ] Color-coded log messages (info, warning, error)
- [ ] Animated icons during downloads
- [ ] Progress in window title bar

---

## Feature Enhancements

### 1. Batch URL Processing
**Priority: High**

**New Feature:**
- [ ] Multi-line URL input
- [ ] Import URLs from text file
- [ ] URL validation before download
- [ ] Duplicate URL detection
- [ ] Pattern-based URL generation (e.g., user profiles pagination)

### 2. Advanced Filtering
**Priority: Medium**

**New Features:**
- [ ] Filter by file size (min/max)
- [ ] Filter by date range (posted date)
- [ ] Filter by file extension (beyond type categories)
- [ ] Custom regex patterns for filenames
- [ ] Exclude patterns (skip files matching criteria)
- [ ] Save filter presets

### 3. Network Configuration
**Priority: Medium**

**New Features:**
- [ ] Proxy support (HTTP, SOCKS)
- [ ] Bandwidth limiting (max download speed)
- [ ] Connection timeout settings
- [ ] Retry configuration per-site
- [ ] User-Agent customization
- [ ] Rate limiting configuration

### 4. Scheduling & Automation
**Priority: Low**

**New Features:**
- [ ] Scheduled downloads (time-based)
- [ ] Watch folders for URL lists
- [ ] Post-download actions (move, organize, notify)
- [ ] Command-line interface for scripting
- [ ] Auto-start with system (optional)

### 5. Site-Specific Features
**Priority: Medium**

**Enhancements:**
- [ ] **Coomer/Kemono**: Favorite users tracking, new post notifications
- [ ] **Erome**: Album detection improvements
- [ ] **Bunkr**: Better file type detection
- [ ] **SimpCity**: Thread pagination improvements
- [ ] **Jpg5**: Gallery support

### 6. Media Organization
**Priority: Medium**

**New Features:**
- [ ] Custom folder structure templates
- [ ] Metadata extraction (EXIF for images)
- [ ] Auto-rename based on metadata
- [ ] Duplicate detection (hash-based)
- [ ] Archive management (auto-extract)

---

## Architecture Improvements

### 1. Refactor UI Components
**Priority: High**

**Proposed Changes:**
- [ ] Split `ui.py` into smaller, focused modules:
  - `main_window.py` - Main application window
  - `url_input.py` - URL input and validation
  - `download_panel.py` - Download controls and progress
  - `log_panel.py` - Logging display
  - `menu_bar.py` - Menu and navigation
  - `status_bar.py` - Footer status display
- [ ] Create widget factory for consistent styling
- [ ] Implement MVC/MVP pattern for better separation

### 2. Standardize Downloader Interface
**Priority: High**

**Proposed Changes:**
- [ ] Create abstract `BaseDownloader` class:
```python
from abc import ABC, abstractmethod
from typing import List

class BaseDownloader(ABC):
    @abstractmethod
    def download_profile(self, url: str, options: DownloadOptions) -> DownloadResult:
        """Download all media from a user profile."""
        pass
    
    @abstractmethod
    def download_post(self, url: str, options: DownloadOptions) -> DownloadResult:
        """Download media from a single post."""
        pass
    
    @abstractmethod
    def get_media_urls(self, url: str) -> List[MediaItem]:
        """Extract media URLs from a page without downloading."""
        pass
    
    @abstractmethod
    def supports_url(self, url: str) -> bool:
        """Check if this downloader can handle the given URL."""
        pass
```
- [ ] Implement consistent error handling
- [ ] Unified progress reporting
- [ ] Plugin architecture for new sites

### 3. Configuration Management
**Priority: Medium**

**Proposed Changes:**
- [ ] Centralized configuration class
- [ ] Configuration schema validation
- [ ] Migration support for config changes
- [ ] Environment variable overrides
- [ ] Per-site configuration options

### 4. Logging System
**Priority: Medium**

**Proposed Changes:**
- [ ] Use Python `logging` module properly
- [ ] Log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Log rotation
- [ ] Structured logging (JSON format option)
- [ ] Separate log files per download session

### 5. Database Improvements
**Priority: Low**

**Proposed Changes:**
- [ ] Add indexes for faster queries
- [ ] Expand schema for metadata storage
- [ ] Add site-specific tables
- [ ] Implement soft delete for history
- [ ] Add user/profile tracking table

---

## Performance Optimizations

### 1. Download Performance
**Priority: Medium**

**Proposed Changes:**
- [ ] Connection pooling optimization
- [ ] Chunk size configuration
- [ ] Resume support for all downloaders
- [ ] Memory usage optimization for large files
- [ ] Async download implementation (optional)

### 2. UI Performance
**Priority: Medium**

**Proposed Changes:**
- [ ] Lazy loading for history/database views
- [ ] Virtual scrolling for large lists
- [ ] Debounced UI updates
- [ ] Background thread for non-UI operations
- [ ] Progress update throttling

### 3. Resource Management
**Priority: Low**

**Proposed Changes:**
- [ ] Image caching for thumbnails
- [ ] Proper cleanup on app close
- [ ] Memory profiling and optimization
- [ ] Disk cache for parsed pages

---

## Configuration & Customization

### 1. User Preferences
**Priority: Medium**

**New Options:**
- [ ] Customizable keyboard shortcuts
- [ ] Window position/size persistence
- [ ] Custom themes (color schemes)
- [ ] Font size adjustment
- [ ] Column visibility in lists

### 2. Download Presets
**Priority: Low**

**New Feature:**
- [ ] Save download configurations as presets
- [ ] Quick-access preset buttons
- [ ] Import/export presets
- [ ] Per-site default presets

### 3. Advanced Settings
**Priority: Low**

**New Options:**
- [ ] Debug mode toggle
- [ ] Performance tuning options
- [ ] Experimental features toggle
- [ ] Developer options (network logging, etc.)

---

## Testing & Quality

### 1. Test Infrastructure
**Priority: High**

**Proposed Implementation:**
- [ ] Unit tests for downloaders
- [ ] UI tests (pytest-qt or similar)
- [ ] Integration tests for end-to-end flows
- [ ] Mock servers for testing without network

### 2. Code Quality
**Priority: Medium**

**Proposed Implementation:**
- [ ] Add type hints throughout codebase
- [ ] Implement linting (flake8, pylint)
- [ ] Add code formatting (black)
- [ ] Documentation strings for all public methods
- [ ] CI/CD pipeline for automated testing

### 3. Error Handling
**Priority: High**

**Proposed Changes:**
- [ ] Comprehensive exception handling
- [ ] User-friendly error messages
- [ ] Error reporting mechanism
- [ ] Crash recovery
- [ ] Graceful degradation

---

## Implementation Priority

### Phase 1: Foundation (High Priority)
1. **Refactor UI architecture** - Split monolithic ui.py
2. **Standardize downloader interface** - Create base class
3. **Batch URL support** - Multi-line input
4. **Download queue manager** - Basic queue controls
5. **Test infrastructure** - Basic unit tests

### Phase 2: Core Features (Medium Priority)
1. **Network configuration** - Proxy, bandwidth limiting
2. **Advanced filtering** - Size, date, custom patterns
3. **Enhanced settings** - Reorganization, presets
4. **History browser** - Search, filter, thumbnails
5. **Logging improvements** - Levels, rotation, export

### Phase 3: Advanced Features (Lower Priority)
1. **Scheduling** - Time-based downloads
2. **System integration** - Tray, notifications
3. **Site-specific enhancements** - Per-site features
4. **Performance optimization** - Async, caching
5. **Custom themes** - User-defined appearance

---

## Notes for Implementation

### Breaking Changes to Consider
- Settings file format changes may require migration
- Database schema changes need upgrade path
- Downloader API changes affect custom extensions

### Backwards Compatibility
- Preserve existing settings when possible
- Provide import tool for old configurations
- Document all breaking changes

### Dependencies to Evaluate
- Consider `httpx` for HTTP client (can replace requests)
  - Benefits: Native async/await support, HTTP/2 support, connection pooling
  - Note: httpx also supports synchronous usage, allowing gradual migration
- Consider `pydantic` for settings validation
  - Benefits: Type safety, automatic validation, serialization
- Evaluate `ttkbootstrap` for enhanced theming
  - Benefits: Modern Bootstrap-like themes, consistent styling
- Consider `pyinstaller` hooks for new dependencies

---

## Feedback & Contributions

This roadmap is a starting point for discussion. Areas that need community input:

1. **Feature prioritization** - What matters most to users?
2. **Site support requests** - Which new sites to add?
3. **UI preferences** - What layout works best?
4. **Performance concerns** - What's slow or resource-heavy?

---

*Last updated: December 2024*
*Version: 0.1 (Draft)*
