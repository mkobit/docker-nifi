# Docker NiFi
This is an unofficial [Apache NiFi](https://nifi.apache.org/) Docker image

* [Docker Hub](#docker-hub)
* [Running Image](#running-image)
# [ListenHTTP Processor](#listenhttp-processor)
* [Usage](#usage)

## Docker Hub
This image is available on Docker Hub at [mkobit/nifi](https://hub.docker.com/r/mkobit/nifi/).

## Running image
To this image and play around with NiFi:

1. Pull `latest` image

        docker pull mkobit/nifi

2. Run image and expose ports.

        # --rm : remove container on exit
        # -i : interactive
        # -t : allocate TTY
        # -p : publish each container port to host port. format: ip:hostPort:containerPort | ip::containerPort | hostPort:containerPort | containerPort
        docker run -it --rm -p 8080-8081:8080-8081 mkobit/personal-nifi

3. Go to local endpoint http://localhost:8080/nifi/

# NiFi Documentation and Guides
These are links to the official NiFi documentation

* [Overview](https://nifi.apache.org/docs.html)
* [User Guide](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html)
* [Expression Language](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)
* [Development Quickstart](https://nifi.apache.org/quickstart.html)
* [Developer's Guide](https://nifi.apache.org/developer-guide.html)
* [System Administrator](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html)

## ListenHTTP Processor
The standard library has a built-in processor for an HTTP endpoint listener. That processor is named [`ListenHTTP`](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi.processors.standard.ListenHTTP/index.html). You should set the **Listening Port** to 8081 if you follow the instructions above to run this image.

## Usage
This image will typically be used as a base image for other NiFi based images. Most people will develop their own NARs as well as their own configuration
