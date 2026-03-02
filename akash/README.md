# Akash SDL Template Library

This library contains 310 production-ready Akash deployment templates organized into 31 categories.

## Quick Start

1. Browse the category subdirectories to find the template you need
2. Pick a template YAML file (e.g., `databases/postgres.yaml`)
3. Check [SECRETS.md](./SECRETS.md) to see what credentials the template requires
4. Provision the required secrets in your DigitalFrontier organization
5. Deploy to Akash using the SDL file

## Secret Provisioning Workflow

Templates that require credentials use `{{PLACEHOLDER}}` syntax in their SDL files. Before deploying, you must provision these placeholders as secrets in your DigitalFrontier (DF) organization.

See [SECRETS.md](./SECRETS.md) for the complete list of `{{PLACEHOLDER}}` names, their descriptions, the DF API key names to use, and which templates reference them.

## Categories

Templates are organized into subdirectories by category. Browse the 31 category folders to find templates by topic:

- Each subdirectory corresponds to an awesome-akash category
- Templates not matched to a known category land in `_uncategorized/`
- Each YAML file is a complete, deployable Akash SDL

## Deployment

To deploy a template to Akash, use the Akash CLI or the DigitalFrontier console:

```bash
## Deploy using the Akash CLI
akash tx deployment create <template.yaml> --from <your-wallet>
```

For full deployment instructions, visit the [Akash Deployment Documentation](https://docs.akash.network/deployments/overview/).

## Support

For help with Akash deployments, secrets provisioning, or template issues:

- Akash documentation: <https://docs.akash.network/>
- DigitalFrontier support: <https://digitalfrontier.app/>
- awesome-akash repository: <https://github.com/akash-network/awesome-akash>
