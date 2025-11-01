#!/bin/bash

# Full Backup Script with ALL Assets
# Includes: Code, Databases, Images, Logos, Profiles, Settings

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="../backups_full/backup_full_${TIMESTAMP}"
PROJECT_ROOT="$(pwd)"

echo "🚀 Starting FULL backup with ALL assets..."
echo "📦 Backup directory: $BACKUP_DIR"

# Create backup directory structure
mkdir -p "$BACKUP_DIR"/{source,databases,images,static,config,docs}

echo "📁 Copying source code..."
# Copy all source files
cp -r templates "$BACKUP_DIR/source/"
cp -r static "$BACKUP_DIR/source/" 2>/dev/null || true
cp *.py "$BACKUP_DIR/source/" 2>/dev/null || true
cp *.sh "$BACKUP_DIR/source/" 2>/dev/null || true

echo "💾 Backing up databases..."
# Copy all SQLite databases
for db in *.db; do
    if [ -f "$db" ]; then
        cp "$db" "$BACKUP_DIR/databases/"
        sqlite3 "$db" .dump > "$BACKUP_DIR/databases/${db%.db}_dump.sql"
        echo "  ✅ $db"
    fi
done

echo "🖼️  Backing up ALL images..."
# Car images
if [ -d "cars" ]; then
    cp -r cars "$BACKUP_DIR/images/"
    echo "  ✅ Car images"
fi

# Uploads
if [ -d "uploads" ]; then
    cp -r uploads "$BACKUP_DIR/images/"
    echo "  ✅ Uploads"
fi

# Static images
if [ -d "static/images" ]; then
    cp -r static/images "$BACKUP_DIR/images/static_images"
    echo "  ✅ Static images"
fi

# Logos
if [ -d "static/logos" ]; then
    cp -r static/logos "$BACKUP_DIR/images/logos"
    echo "  ✅ Supplier logos"
fi

# Profile pictures
if [ -d "static/profiles" ]; then
    cp -r static/profiles "$BACKUP_DIR/images/profiles"
    echo "  ✅ Profile pictures"
fi

# Car pictures
if [ -d "static/car_pictures" ]; then
    cp -r static/car_pictures "$BACKUP_DIR/images/car_pictures"
    echo "  ✅ Car pictures"
fi

echo "⚙️  Backing up configuration files..."
# Configuration files
cp .env "$BACKUP_DIR/config/" 2>/dev/null || echo "  ⚠️  No .env file"
cp requirements.txt "$BACKUP_DIR/config/" 2>/dev/null || true
cp render.yaml "$BACKUP_DIR/config/" 2>/dev/null || true
cp Dockerfile "$BACKUP_DIR/config/" 2>/dev/null || true
cp docker-compose.yml "$BACKUP_DIR/config/" 2>/dev/null || true

# Excel files
cp *.xlsx "$BACKUP_DIR/config/" 2>/dev/null || true

echo "📚 Backing up documentation..."
# Documentation
cp *.md "$BACKUP_DIR/docs/" 2>/dev/null || true
cp *.txt "$BACKUP_DIR/docs/" 2>/dev/null || true

echo "🔧 Creating Git bundle..."
# Git bundle with full history
git bundle create "$BACKUP_DIR/git_repository.bundle" --all 2>/dev/null || echo "  ⚠️  Git bundle failed"

echo "📋 Creating manifest..."
# Create manifest
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
FULL BACKUP MANIFEST
====================
Timestamp: $TIMESTAMP
Date: $(date)
Project: Rental Price Tracker Per Day

CONTENTS:
---------
✅ Source Code (templates/, *.py, *.sh)
✅ Databases (*.db + SQL dumps)
✅ Car Images (cars/)
✅ Uploads (uploads/)
✅ Static Images (static/images/)
✅ Supplier Logos (static/logos/)
✅ Profile Pictures (static/profiles/)
✅ Car Pictures (static/car_pictures/)
✅ Configuration (.env, requirements.txt, render.yaml, Dockerfile)
✅ Excel Files (*.xlsx)
✅ Documentation (*.md, *.txt)
✅ Git Repository Bundle (full history)

STATISTICS:
-----------
EOF

# Add statistics
echo "Source files: $(find "$BACKUP_DIR/source" -type f 2>/dev/null | wc -l)" >> "$BACKUP_DIR/MANIFEST.txt"
echo "Database files: $(find "$BACKUP_DIR/databases" -type f 2>/dev/null | wc -l)" >> "$BACKUP_DIR/MANIFEST.txt"
echo "Image files: $(find "$BACKUP_DIR/images" -type f 2>/dev/null | wc -l)" >> "$BACKUP_DIR/MANIFEST.txt"
echo "Config files: $(find "$BACKUP_DIR/config" -type f 2>/dev/null | wc -l)" >> "$BACKUP_DIR/MANIFEST.txt"
echo "Total size: $(du -sh "$BACKUP_DIR" | cut -f1)" >> "$BACKUP_DIR/MANIFEST.txt"

echo "📦 Creating compressed archive..."
# Create tar.gz
cd "$(dirname "$BACKUP_DIR")"
tar -czf "backup_full_${TIMESTAMP}.tar.gz" "backup_full_${TIMESTAMP}"

echo ""
echo "✅ BACKUP COMPLETE!"
echo "📁 Location: $BACKUP_DIR"
echo "📦 Archive: $(dirname "$BACKUP_DIR")/backup_full_${TIMESTAMP}.tar.gz"
echo "📊 Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo ""
echo "📋 Manifest:"
cat "$BACKUP_DIR/MANIFEST.txt"
