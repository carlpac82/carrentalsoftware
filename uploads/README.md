# Uploads Directory

This directory contains user-uploaded files that should be persisted.

## Structure

```
uploads/
├── profiles/     # User profile pictures
└── vehicles/     # Vehicle images (if any)
```

## Important for Render Deployment

⚠️ **Files in this directory are NOT included in git** (see `.gitignore`)

### To preserve uploads on Render:

1. **Use Render Disk** (recommended):
   - Add a Disk to your service in Render dashboard
   - Mount it to `/opt/render/project/src/uploads`
   - Files will persist across deploys

2. **Or use external storage**:
   - AWS S3
   - Cloudinary
   - Google Cloud Storage

### Backup Profile Pictures

Before deploying, backup existing profile pictures:

```bash
# Local backup
tar -czf profile_pictures_backup.tar.gz uploads/profiles/

# Restore after deploy
tar -xzf profile_pictures_backup.tar.gz
```

## Environment Variables

- `UPLOADS_ROOT`: Override default uploads directory (default: `./uploads`)
- `DATA_DIR`: Parent directory for all data (default: current directory)
