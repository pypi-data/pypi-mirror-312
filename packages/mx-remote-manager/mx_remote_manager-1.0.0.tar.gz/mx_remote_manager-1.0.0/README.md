# MX Remote Manager

Application for managing MX Remote compatible devices.

## Installation

Run `install-pip.sh` if you're building from source. Alternatively you can use one of the prebuilt binaries.
These binaries can be built by calling `build-dist.sh`.

Please note that the prebuilt binaries will take more time to start, while the version installed by pip will run much faster.

## Application
The GUI application is started by running `mxr-ui` and the console application by running `mxr`.

The application also includes methods for debugging MX Remote networks:
* The console application will always dump all received frames in human readable form on the console
* GUI application that dumps all received frames in human readable form on the console: `mxr -u 1`
* To dump these frames in a file `mxr -u 1 -o /path/to/file.txt`
* Import frames captured by MatrixOS and dump the frames: `mxr -i /path/to/file.bin`

All command line options:
```
usage: mxr [-h] [-i INPUT] [-f FILTER] [-o OUTPUT] [-l LOCAL_IP] [-b BROADCAST] [-u UI]

MX Remote Manager / Debugger

options:
  -h, --help    show this help message and exit
  -i INPUT      capture file to process
  -f FILTER     ip address to process in the capture file
  -o OUTPUT     write output to a file
  -l LOCAL_IP   local ip address of the network interface to use
  -b BROADCAST  use broadcast mode instead of multicast mode
  -u UI         show the user interface
```

The user interface option and `mxr-ui` application are only available when `mx_remote_manager` is installed after installing `mx_remote`.
Plain `mx_remote` only includes the command line version of `mxr`.
