FROM google/dart-runtime-base

WORKDIR /project/app

# Add the pubspec.yaml files for each local package.
#ADD pkg/my-package-1/pubspec.yaml /project/pkg/my-package-1/
#ADD pkg/my-package-2/pubspec.yaml /project/pkg/my-package-2/

# Template for adding the application and local packages.
ADD pubspec.* /project/app/
RUN pub get

ADD ./bin /project/app
ADD ./lib /project/app

RUN pub get --offline
