#!/bin/bash -ex
#
# Usage:
#   ./build.sh [output_file]


target_archive_file=${1:-virtuscale.tar.gz}

pushd "$(dirname "$0")"
dist_dir=$(mktemp -d)
python3 setup.py sdist --format=gztar --dist-dir "$dist_dir"
cp "$dist_dir"/*.tar.gz "$target_archive_file"
popd
