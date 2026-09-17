# das element resources

Useful example scripts and Python hooks for customizing [**das element**](https://das-element.com).

> Browse the full [das element documentation](https://docu.das-element.com) for setup instructions, configuration details, and API references.

## Contents

- [Transcoding examples and templates](#transcoding-examples-and-templates)
- [Python hooks](#python-hooks)

## Transcoding examples and templates

Ready-to-use examples for proxy generation and Nuke integrations:

| Resource | Description |
| --- | --- |
| [Proxy generation scripts](https://github.com/das-element/resources/tree/main/scripts/custom/examples) | Example scripts for creating proxies and customizing transcoding workflows. |
| [Foundry Nuke templates](https://github.com/das-element/resources/tree/main/scripts/custom/examples/nuke) | Example templates for integrating **das element** with The Foundry Nuke. |

## Python hooks

Example hooks for extending ingest, render submission, and metadata workflows:

| Resource | Description |
| --- | --- |
| [Ingest tagging](https://github.com/das-element/resources/tree/main/scripts/hooks/examples/ingest) | Automatically create tags from a folder structure. |
| [AWS Deadline submission](https://github.com/das-element/resources/tree/main/scripts/hooks/examples/deadline) | Retrieve job dependencies when submitting jobs to AWS Deadline. |
| [Autodesk ShotGrid export](https://github.com/das-element/resources/tree/main/scripts/hooks/examples/shotgrid) | Export data as a CSV for use with Autodesk ShotGrid. |

## Getting started

1. Choose an example from the sections above.
2. Review the example's README and source code.
3. Copy or adapt the script for your **das element** workflow.
4. Refer to the [documentation](https://docu.das-element.com) for configuration and integration details.

## Contributing

Improvements and additional examples are welcome. Please open an issue or pull request with a clear description of the use case and any required setup.
