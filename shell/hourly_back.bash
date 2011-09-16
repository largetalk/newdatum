#!/bin/bash

hour=$(( $( date +%k ) % 8 ))
PASSWORD=ellis pg_dump --clean --format=plain --inserts --column-inserts --username ellis --file=media/tmp/backup.$hour
rsync -av media/tmp/backup.* ellis@yanzi:
rsync -av media/upload/ ellis@yanzi:upload/
