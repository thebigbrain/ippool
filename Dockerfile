FROM python:3.7.3-alpine3.9

WORKDIR /app

# Add the pubspec.yaml files for each local package.
#ADD pkg/my-package-1/pubspec.yaml /project/pkg/my-package-1/
#ADD pkg/my-package-2/pubspec.yaml /project/pkg/my-package-2/

# Template for adding the application and local packages.
ADD . /app

ENTRYPOINT ["/usr/local/bin/python", "/app/tools/crawl.py"]
