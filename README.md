# das element resources

<<<<<<< Updated upstream
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
=======
![das element resources](das-element-resources.png)

Examples, utilities, and integration hooks for customizing **das element** workflows.
Use these files as starting points for your own ingest, transcoding, automation, and
production pipeline integrations.

> These examples are provided as templates. Review and adapt paths, applications,
> credentials, and production-specific behavior before deploying them.

## Start here

1. Browse the [das element documentation](https://docu.das-element.com) for the
	concepts and configuration options behind these examples.
2. Choose the area that matches your workflow below.
3. Copy an example into your custom configuration and adapt it to your environment.

## What's included

### Custom scripts

The [`scripts/custom/examples`](scripts/custom/examples) directory contains scripts
for common media-processing tasks:

- [`create_proxy.py`](scripts/custom/examples/create_proxy.py) - create proxy media
- [`create_thumbnail.py`](scripts/custom/examples/create_thumbnail.py) - create thumbnails
- [`create_filmstrip.py`](scripts/custom/examples/create_filmstrip.py) - create a filmstrip
- [`create_filmstrip_batch.py`](scripts/custom/examples/create_filmstrip_batch.py) - create filmstrips in batches
- [`copy_main.py`](scripts/custom/examples/copy_main.py) - copy media as part of a custom workflow

For workflows involving [The Foundry Nuke](https://www.foundry.com/products/nuke),
see the [Nuke examples](scripts/custom/examples/nuke).

### Hooks

The [`scripts/hooks/examples`](scripts/hooks/examples) directory contains lifecycle
hooks that extend das element behavior:

- [`ingest`](scripts/hooks/examples/ingest) - customize ingest loading behavior
- [`deadline`](scripts/hooks/examples/deadline) - integrate with AWS Deadline rendering
- [`shotgrid`](scripts/hooks/examples/shotgrid) - export data to Autodesk ShotGrid
- [`gallery`](scripts/hooks/examples/gallery) - customize gallery loading and drag behavior
- [`delete_element`](scripts/hooks/examples/delete_element) - respond before or after an element is deleted
- [`actions`](scripts/hooks/examples/actions) - add custom actions

### Utilities and code snippets

The [`misc`](misc) directory contains standalone utilities and smaller examples,
including:

- Copying main media and proxies to FTP
- Creating custom tags
- Launching software with a specific configuration
- Importing media from the clipboard
- Reading tags from metadata with `ffprobe`
- Ingesting media from ingest logs
- Building a hierarchy from a folder structure
- A custom Nuke drop handler

## Repository layout

```text
misc/                       Standalone utilities and code snippets
scripts/custom/examples/   Custom media-processing scripts
scripts/hooks/examples/    Lifecycle hook examples
```

## Contributing

Keep examples focused, document required configuration, and avoid committing
credentials or environment-specific paths. Contributions that improve an existing
example or add a broadly useful integration are welcome.
>>>>>>> Stashed changes
