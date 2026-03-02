# Ghost with Filebase Backup

Deploy a Ghost blog with automatic IPFS backup via Filebase.

## Features

- Ghost blogging system
- Automatic data backup to Filebase (IPFS-based S3-compatible storage)
- Encrypted backup support
- Optional email service configuration

## Required Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `url` | `http://yourdomain.com` | Ghost blog URL (must match the `accept` domain) |
| `NODE_ENV` | `production` | Runtime environment |
| `FILEBASE_BUCKET` | `my-ghost-backup` | Filebase bucket name |
| `FILEBASE_ENDPOINT` | `https://s3.filebase.com` | Filebase S3 endpoint |
| `FILEBASE_ACCESS_KEY_ID` | `your-access-key` | Filebase access key ID |
| `FILEBASE_SECRET_ACCESS_KEY` | `your-secret-key` | Filebase secret key |
| `BACKUP_ENCRYPTION_PASSWORD` | `strong-password` | Database backup encryption password |

## Optional Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `FILEBASE_BACKUP_PATH` | `my-backup` | Backup directory path prefix |

Without `FILEBASE_BACKUP_PATH`: backups go to `s3://bucket/images` and `s3://bucket/data`.
With it set to `my-backup`: backups go to `s3://bucket/my-backup/images` and `s3://bucket/my-backup/data`.

## Email Configuration (Optional)

Ghost uses double underscores (`__`) as nested config separators:

```yaml
env:
  - mail__transport=SMTP
  - mail__options__host=smtp.resend.com
  - mail__options__port=587
  - mail__options__secure=false
  - mail__options__requireTLS=true
  - mail__options__auth__user=resend
  - mail__options__auth__pass=re_xxxxxxxxxxxxx
  - mail__from=noreply@resend.dev
```

## Setup Steps

1. Register at [Filebase](https://filebase.com) and create a bucket
2. Replace `changeme.com` with your domain in the `accept` field
3. Fill in the Filebase environment variables
4. Generate an encryption password: `openssl rand -base64 32`
5. Deploy via Blazing Core
6. Point your domain DNS to the provider-assigned URI

## More Information

See the upstream project: <https://github.com/zhajingwen/ghost-ipfs-bkup>
