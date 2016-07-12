#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from git import Repo
from yaml import load
from shutil import rmtree
from subprocess import call

config_file = ""
services = []


def main():
    args = define_options()

    if args.file:
        set_file(args.file)

    if args.services:
        set_services(args.services)

    build_images()


def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="Choose the yaml file of configuration (default: ./config/services.yaml)",
                        default="./config/services.yaml")
    parser.add_argument("-s", "--services", help="Define which services on yaml file will be configured (default: all)",
                        nargs="+", default=["all"])
    return parser.parse_args()


def set_file(yaml_file):
    global config_file
    config_file = yaml_file


def set_services(service):
    global services
    for value in service:
        services.append(value)


def get_service(repository, branch, containerRepository, directory):
    print("> Cloning the {}".format(containerRepository))
    Repo.clone_from("git@github.com:creativesterminal/{}.git".format(containerRepository),
                    os.path.join(directory, containerRepository))

    print("> Cloning the {}".format(repository))
    Repo.clone_from("git@github.com:creativesterminal/{}.git".format(repository),
                    os.path.join(directory, containerRepository, repository), branch=branch)


def build_image(service, containerRepository, tag):
    if service == "web":
        call(["npm", "install", "--prefix", os.path.join(containerRepository, service)+os.sep])

    if service.endswith('-service'):
        image = "registry.stage.creativesterminal.com/services/{}:{}".format(service[:-8], tag)
        call(["docker", "build", "-t", image, containerRepository])
    else:
        image = "registry.stage.creativesterminal.com/{}:{}".format(service, tag)
        call(["docker", "build", "-t", image, containerRepository])

    return image


def push_image(image):
    call(["docker", "push", image])


def deploy_image(service, image):
    call(["docker", "run", "-it", "--rm", "--env-file=./local.env",
          "registry.stage.creativesterminal.com/tools/ecs-deploy", "-c", "cterm-ecs-cluster", "-n", service,
          "-i", image])


def build_images():
    stream = load(file(config_file, 'r'))

    for key, value in stream.iteritems():
        if key not in services and 'all' not in services:
            continue

        get_service(value['repository'], value['branch'], value['container-repository'], './repositories')

        print("> Building the image")
        image = build_image(key, value['container-repository'], value['version'])

        print(">  Pushing the image")
        push_image(image)
        deploy_image(value['aws-service'], image)
        rmtree("./{}".format(value['container-repository']))

    sys.exit(0)


if __name__ == "__main__":
    main()
