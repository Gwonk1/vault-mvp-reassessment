#!/usr/bin/env bash
# Watch the channel and the running analyses together.
cd ~/projects/Vault
exec tail -n 40 -F channel/TRANSCRIPT.md results/surface.log results/prot_final.log
