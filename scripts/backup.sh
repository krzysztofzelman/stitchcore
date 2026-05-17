#!/bin/bash
# StitchCore Backup Script
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "Creating database backup..."
docker-compose exec -T postgres pg_dump -U stitchcore stitchcore > "$BACKUP_DIR/stitchcore_db_$TIMESTAMP.sql"

echo "Compressing backup..."
gzip "$BACKUP_DIR/stitchcore_db_$TIMESTAMP.sql"

echo "Backup created: $BACKUP_DIR/stitchcore_db_$TIMESTAMP.sql.gz"
echo "Done!"
