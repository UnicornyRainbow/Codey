#!/bin/sh

clear
rm -rf repo
echo "##########################  building  package  ##########################"
flatpak-builder --force-clean --repo=repo build io.github.unicornyrainbow.codey.yml
flatpak build-bundle repo codey.flatpak io.github.unicornyrainbow.codey
echo "#########################  deleting old pakage  #########################"
flatpak remove --force-remove --delete-data --noninteractive -y codey
echo "########################  installing new pakage  ########################"
flatpak-builder --user --install --force-clean build "io.github.unicornyrainbow.codey.yml"