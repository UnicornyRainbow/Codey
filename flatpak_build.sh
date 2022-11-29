#!/bin/sh

flatpak-builder --user --install --force-clean build "io.github.unicornyrainbow.codey.yml"
flatpak run io.github.unicornyrainbow.codey
