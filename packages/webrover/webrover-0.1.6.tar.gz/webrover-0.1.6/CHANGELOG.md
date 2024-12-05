# Changelog

All notable changes to WebRover will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] - 2024-11-29

### Added
- CHANGELOG.md to track version history
- MANIFEST.in for proper package file inclusion
- Better package metadata handling

### Changed
- Updated setup.py to include CHANGELOG.md and LICENSE
- Improved package distribution structure

## [0.1.5] - 2024-11-29

### Added
- Progress bar with tqdm integration
- Display of dataset save location after completion
- Final statistics summary display

### Changed
- Updated dependencies to include tqdm
- Enhanced progress tracking format

## [0.1.4] - 2024-11-29

### Added
- Enhanced logging with emojis for better visibility
- Detailed status messages for each operation
- Clear success/error indicators

### Changed
- Improved log message formatting
- More descriptive process status updates

## [0.1.3] - 2024-11-29

### Added
- Display of current website being scraped
- Loading status indicators during scraping
- Better error reporting

### Changed
- Improved console output readability
- Enhanced error message clarity

## [0.1.2] - 2024-11-29

### Added
- Detailed logging for each scraping step
- Process start/end notifications
- Status updates for URL collection

### Fixed
- Character encoding issues in logging
- Console output formatting

## [0.1.1] - 2024-11-28

### Added
- Basic logging functionality
- Support for multiple input formats (JSON, YAML, TXT, MD)
- Async web scraping capabilities
- Rate limiting for Google searches
- Error handling and statistics

### Fixed
- Encoding issues in setup.py
- Package installation dependencies

## [0.1.0] - 2024-11-28

### Added
- Initial release
- Basic web scraping functionality
- Google search integration
- Dataset generation in JSONL format
- Basic example scripts 