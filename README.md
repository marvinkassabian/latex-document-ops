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

Secrets:

- `mega_io_username`
- `mega_io_password`
- `proton_username`
- `proton_password`
- `proton_mailbox_password`

## Available Actions

- `.github/actions/validate-release-version`
- `.github/actions/download-release-pdfs`
- `.github/actions/configure-rclone-mega`
- `.github/actions/configure-rclone-proton`
- `.github/actions/upload-pdfs-mega`
- `.github/actions/upload-pdfs-proton`

## Caller Pattern

Keep triggers, repository-variable evaluation, and secrets in the document repository. Call these workflows with explicit inputs.

Current callers can reference this repository at `@main`, but that should be replaced with a release tag or pinned commit SHA once the first stable version is cut.
