#!/bin/sh
# flatpak-pip-generator --requirements-file=requirements.txt
rm -rf repo
mkdir repo
flatpak-builder build io.github.unicorn.codey.yml --force-clean --repo=repo
flatpak build-bundle repo codey.flatpak io.github.unicorn.codey

if [ "$1" = "-i" ] || [ "$1" = "--install" ]
then
  flatpak remove --force-remove --delete-data --noninteractive -y codey
  flatpak-builder --user --install --force-clean build "io.github.unicorn.codey.yml"
fi

if [ "$2" = "-r" ] || [ "$2" = "--run" ]
then
  flatpak run io.github.unicorn.codey
fi
