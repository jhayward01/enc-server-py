#!/bin/bash

# Integration Test #1
docker compose up -d --build
make feclient &> /tmp/itest1.full
cat /tmp/itest1.full | grep -v DEBUG | cut -f4- -d' ' | grep -v "Store received" > /tmp/itest1.actual
diff /tmp/itest1.actual test/itest1.expect
docker compose down
