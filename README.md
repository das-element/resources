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
