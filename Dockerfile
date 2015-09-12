FROM java:8

ENV NIFI_VERSION=0.2.1 \
        NIFI_HOME=/opt/nifi

# Picked recommended mirror from Apache for the distribution.
# Import Joe Witt's (joewitt@apache.org) key for gpg signature verification
# Can't currently verify the SHA1 because the https://dist.apache.org/repos/dist/release/nifi/$NIFI_VERSION/nifi-0.2.1-bin.tar.gz.sha1 is incorrectly truncated
RUN set -x \
        && gpg --keyserver pgpkeys.mit.edu --recv-key 4F811A1A \
        && curl -SL http://mirror.symnds.com/software/Apache/nifi/0.2.1/nifi-0.2.1-bin.tar.gz -o /tmp/nifi-bin.tar.gz \
        && curl -SL https://dist.apache.org/repos/dist/release/nifi/0.2.1/nifi-0.2.1-bin.tar.gz.asc -o /tmp/nifi-bin.tar.gz.asc \
        && curl -SL https://dist.apache.org/repos/dist/release/nifi/0.2.1/nifi-0.2.1-bin.tar.gz.md5 -o /tmp/nifi-bin.tar.gz.md5 \
        && gpg --verify /tmp/nifi-bin.tar.gz.asc /tmp/nifi-bin.tar.gz \
        && echo "$(cat /tmp/nifi-bin.tar.gz.md5) /tmp/nifi-bin.tar.gz" | md5sum -c - \
        && mkdir -p /opt/nifi \
        && tar -z -x -f /tmp/nifi-bin.tar.gz -C /opt/nifi --strip-components=1 \
        && rm /tmp/nifi-bin.tar.gz /tmp/nifi-bin.tar.gz.asc /tmp/nifi-bin.tar.gz.md5

# Add volumes and replace props in the file?

WORKDIR $NIFI_HOME
EXPOSE 8080 8081
ENTRYPOINT ["bin/nifi.sh"]
CMD ["run"]
