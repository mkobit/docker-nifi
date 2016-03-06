FROM ruby:1.9.3

RUN gem install travis --no-rdoc --no-ri
VOLUME /tmp/travis-workdir
WORKDIR /tmp/travis-workdir
ENTRYPOINT ["travis"]
