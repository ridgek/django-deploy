#!/bin/sh

usage()
{
cat << EOF

Bootstrap

$0 task

Tasks:
  build
  clean
EOF
}

ROOT=`pwd`
VENV=$ROOT/venv
DPKG_REQS=$ROOT/packages.txt
PIP_REQS=$ROOT/requirements.txt

build_packages()
{
    sudo apt-get -qq update
    sudo apt-get -qq install $(< $DPKG_REQS)
}

build_virtualenv()
{   
    virtualenv $VENV
    . $VENV/bin/activate
    pip install -r $PIP_REQS
    mkdir -p $ROOT/log
}

clean_virtualenv()
{
    rm -rf $VENV
}

case "$1" in
    build)
        build_packages
        build_virtualenv
        ;;
    clean)
        clean_virtualenv
        ;;
    *)
        usage
        ;;
esac