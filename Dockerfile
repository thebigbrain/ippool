FROM google/dart

WORKDIR /app

ENV PUB_HOSTED_URL "https://mirrors.tuna.tsinghua.edu.cn/dart-pub/"

# Add the pubspec.yaml files for each local package.
#ADD pkg/my-package-1/pubspec.yaml /project/pkg/my-package-1/
#ADD pkg/my-package-2/pubspec.yaml /project/pkg/my-package-2/

# Template for adding the application and local packages.
ADD pubspec.* /app/
RUN pub get

ADD . /app

RUN pub get --offline

ENTRYPOINT ["/usr/bin/dart", "/app/bin/crawl.dart"]
