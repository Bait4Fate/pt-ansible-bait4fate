#!/bin/bash
set -e

cat <<EOF >> /var/lib/postgresql/data/postgresql.conf
listen_addresses = '*'
wal_level = replica
max_wal_senders = 3
wal_keep_size = 16
wal_log_hints = on
log_replication_commands = on
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%a.log'
log_truncate_on_rotation = on
log_rotation_age = 0
log_rotation_size = 0
EOF

cat <<EOF >> /var/lib/postgresql/data/pg_hba.conf
host replication all 0.0.0.0/0 md5
host all all 0.0.0.0/0 md5
EOF
