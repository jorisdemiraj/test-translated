# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- added endpoint for gisky to get results

### Fixed

## [1.1.9] - 2023-03-3
### Added 
- added time_shift parameter for ssi algorithm


### Fixed


## [1.1.8] - 2023-02-14

### Added

- Added network filter for structure
- Added new algorithm SSI for OMA 
- Added logging rotator file handler by time
- Added default config parameters for SSI algorithm
- Added log streamHandler
- Added health check api endpoint
- Added ssi get endpoint to get default ssi parameters
- SSI algorithm integration
- Added permission OMA checking
- Added kafka internal notification system between processes
- Added websocket communication with client
- Secured websocket communication
### Fixed

- Code refactoring ssi and fdd library
- Fixed exception handling in structures flow 
- code cleaning and code refactoring

### Changed

- Fixed (removed) user_id in create run/structures

## [1.1.2] - 2022-06-25

### Added

- Acceleration file handler, saved on disk (efs on aws)
- FDD method analysis for OMA
- Logs download for admin 
- Added title and description to run model

### Changed

- Fixed ValueError: zero-size array to reduction operation maximum which has no identity in FDD algorithm
- Fixed bool display variable in pickpeaks algorithm



[unreleased]: https://github.com/sensoworks/OMA/tree/feature/OMA-sensoworks-integration
[1.1.3]: https://github.com/sensoworks/OMA/tree/development


