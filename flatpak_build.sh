#!/bin/sh


echo "building package...................."
flatpak-builder build io.github.unicornyrainbow.codey.yml --force-clean
echo "making .flatpak file..............."
rm -rf repo
flatpak-builder --force-clean --repo=repo build io.github.unicornyrainbow.codey.yml	
flatpak build-bundle repo codey.flatpak io.github.unicornyrainbow.codey
echo "installing........................"
flatpak remove --force-remove --delete-data --noninteractive -y codey
flatpak-builder --user --install --force-clean build "io.github.unicornyrainbow.codey.yml"