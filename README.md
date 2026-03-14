# LaTeX Document Ops

Reusable GitHub Actions workflows and composite actions for LaTeX document repositories.

This repository is intended to hold shared automation for:

- building LaTeX PDFs in GitHub Actions
- publishing GitHub Releases
- downloading release PDF assets
- uploading PDFs to Mega.io and Proton Drive
- keeping document repositories focused on source, assets, and local build ergonomics

## Available Workflows

### `.github/workflows/build.yml`

Reusable build workflow for LaTeX repositories.

Inputs:

- `source_repository`
- `source_ref`
- `build_command`
- `artifact_path`
- `artifact_name`
- `strict_build`
- `clean_command`
- `enable_pages`
- `artifact_retention_days`

### `.github/workflows/release.yml`

Reusable release workflow for LaTeX repositories.

Inputs:

- `source_repository`
- `source_ref`
- `release_tag`
- `build_command`
- `artifact_path`
- `artifact_name`
- `strict_build`
- `clean_command`
- `enable_github_release`
- `generate_release_notes`
- `enable_version_validation`
- `cloud_upload_source`
- `enable_mega_upload`
- `mega_target_path`
- `enable_proton_upload`
- `proton_target_path`
- `sections_dir`
- `frontmatter_dir`

Secrets:

- `mega_io_username`
- `mega_io_password`
- `proton_username`
- `proton_password`
- `proton_mailbox_password`

### `.github/workflows/upload-cloud.yml`

Reusable cloud upload workflow invoked by the release workflow.

Inputs:

- `provider` (`mega` or `proton`)
- `source_repository`
- `source_ref`
- `release_tag`
- `source` (`artifact` or `release`)
- `artifact_name`
- `target_path`
- `sections_dir`
- `frontmatter_dir`

Secrets (optional fallback path):

- `mega_io_username`
- `mega_io_password`
- `proton_username`
- `proton_password`
- `proton_mailbox_password`

Behavior and requirements:

- Automatically selects a GitHub Environment based on `provider`:
  - Mega uploads use `mega-io` by default
  - Proton uploads use `proton-drive` by default
- Environment names can be overridden with caller-repo variables:
  - `MEGA_IO_ENVIRONMENT`
  - `PROTON_DRIVE_ENVIRONMENT`
- Credentials are resolved in this order:
  - environment/repository secrets with uppercase names (`MEGA_IO_USERNAME`, `MEGA_IO_PASSWORD`, `PROTON_USERNAME`, `PROTON_PASSWORD`, `PROTON_MAILBOX_PASSWORD`)
  - explicit `workflow_call` secrets (lowercase names above)
- A preflight credential validation step fails early with actionable messages when required secrets are missing.

## Available Actions

- `.github/actions/validate-release-version`
- `.github/actions/download-release-pdfs`
- `.github/actions/configure-rclone-mega`
- `.github/actions/configure-rclone-proton`
- `.github/actions/upload-pdfs-mega`
- `.github/actions/upload-pdfs-proton`

Action notes:

- `configure-rclone-mega` validates that username/password are present, creates the `mega` remote via `rclone config create`, and verifies login before upload.
- `upload-pdfs-mega` purges the release target path when present and performs a single filtered `rclone copy` for PDF artifacts.

## Caller Pattern

Keep triggers, repository-variable evaluation, and opt-in feature flags in the document repository. Call these workflows with explicit inputs.

For cloud uploads, prefer environment-scoped credentials in the caller repository (`mega-io` and `proton-drive`) and use repository variables only to override environment names when necessary.

Current callers can reference this repository at `@main`, but that should be replaced with a release tag or pinned commit SHA once the first stable version is cut.
