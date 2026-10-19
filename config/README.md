# Configuration examples

The hand-reviewed, credential-free [`environment.env.example`](environment.env.example) mirrors the root [`.env.example`](../.env.example). It documents environment variable names; Python does not automatically load it. Export variables as described in the [README](../README.md).

Audio selection and GPIO/servo settings remain explicit Python constants/literals; see [configuration](../docs/configuration.md). No private `.asoundrc`, shell startup files, SSH files, machine identifiers, boot overlays, or udev rules were copied. Device IDs must be discovered on the target Pi. No system configuration changes are made automatically.
