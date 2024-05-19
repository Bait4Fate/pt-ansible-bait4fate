#!/bin/bash
set -e
if [ -z "$(ls -A /var/lib/postgresql/data)" ]; then
   until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=master --port=5432
      do
      echo 'Waiting for primary to connect...'
      sleep 1s
      done
      echo 'Backup done, starting replica...'
      chmod 0700 /var/lib/postgresql/data
fi

cat <<EOF >> /var/lib/postgresql/data/postgresql.conf
wal_log_hints = on
log_replication_commands = on
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%a.log'
log_truncate_on_rotation = on
log_rotation_age = 0
log_rotation_size = 0
EOF

chown -R postgres:postgres /var/lib/postgresql/data
gosu postgres postgres
