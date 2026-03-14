# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

## [0.2.0] - 2026-03-14

### Added
- Dedicated reusable workflows for GitHub Pages publishing and Mega.io uploads
- GitHub release note category configuration in `.github/release.yml`

### Changed
- Cloud upload automation was split into provider-specific workflows, including a renamed Proton workflow file
- The reusable release workflow now focuses on build-and-release responsibilities while provider uploads run in separate reusable workflows
- Removed the embedded repository hook scripts from `.github/.githooks`


## [0.1.0] - 2026-03-14

### Added
- Reusable workflows for builds, releases, and cloud uploads
- Composite actions for version checks, downloads, and uploads
- Commit and release prompts plus local Git hooks
- Root VERSION and CHANGELOG files for tagged releases

### Changed
- Cloud uploads now support env-scoped and repo-scoped creds
- README now documents inputs, actions, and credential rules

### Fixed
- Mega uploads now validate login and replace target contents
- Secret validation now fails fast with normalized inputs
- Proton mailbox passwords are optional when not required
