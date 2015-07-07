## Nagios plugin for dCache pools

This nagios plugin checks the status of dcache pools with the following rules:
 
 * if any of the pools is disabled the exit code is *critical*;
 * if the number of queued movers of any pool is higher that the given *warning* (`-w`) or *critical* (`-c`) threshold, the relative exit code is returned.

For example:

```
./check_movers.py --pools poolhost1_01,poolhost1_02 \
--server dcache-head.my.domain -w 0 -c 10
```

will generate a *warning* if any mover is queued and a *critical* if more than 10.