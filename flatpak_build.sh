#!/bin/sh


for args in $*
do
	if [ $args = "-h" ] || [ "$args" = "--help" ]
	then
		echo -e "-h, --help\t\tDisplay this help"
		echo -e "-m, --make\t\tMakes a .flatpak file"
		echo -e "-i, --install\t\tDirectly install for current user"
		echo -e "-r, --run\t\tRun the app"
	else
		flatpak-builder build io.github.unicorn.codey.yml --force-clean
		if [ $args = "-m" ] || [ $args = "--make" ]
		then
			rm -rf repo
			flatpak-builder --force-clean --repo=repo build io.github.unicorn.codey.yml	
			flatpak build-bundle repo codey.flatpak io.github.unicorn.codey
		fi

		if [ $args = "-i" ] || [ $args = "--install" ]
		then
			flatpak remove --force-remove --delete-data --noninteractive -y codey
			flatpak-builder --user --install --force-clean build "io.github.unicorn.codey.yml"
		fi
	fi
done

for args in $*
do
	if [ "$args" = "-r" ] || [ "$args" = "--run" ]
	then
		flatpak run io.github.unicorn.codey
	fi
done
