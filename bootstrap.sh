#!/bin/bash
echo "bootstrapping all required files for the flatpak."
required_files=("codey.py" "codey.config" "run.sh" "io.github.unicorn.codey.desktop" "io.github.unicorn.codey.appdata.xml" "io.github.unicorn.codey.png" "LICENSE.txt")
gitlink="https://raw.githubusercontent.com/blackmoonboy/Codey/master/"
mkdir "src"
for file in "${required_files[@]}"
do
  rm "$file"
  current_link="${gitlink}""${file}"
  curl "$current_link" > "$file"
done
echo "finished the download of all required files for the flatpak."

