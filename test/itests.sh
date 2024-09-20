#!/bin/bash

# Integration Test #1
make feclient &> /tmp/itest1.full
grep -v DEBUG < /tmp/itest1.full | cut -f4- -d' ' | grep -v "Store received" > /tmp/itest1.actual
diff /tmp/itest1.actual test/itest1.expect
