# Visum Project

## Contents

1. [Requirements](#requirements)
   * [Host setup](#host-setup)
2. [Usage](#usage)
   * [Bringing up the stack](#bringing-up-the-stack)
3. [Configuration](#configuration)
   * [How can I tune the Kibana configuration ?](#how-can-i-tune-the-kibana-configuration)
   * [How can I tune the Elasticsearch configuration ?](#how-can-i-tune-the-elasticsearch-configuration)
   * [How can I scale out the Elasticsearch cluster ?](#how-can-i-scale-out-the-elasticsearch-cluster)
4. [Storage](#storage)
   * [How can I persist Elasticsearch data?](#how-can-i-persist-elasticsearch-data)
5. [Upgrade](#upgrade)
   * [Using a newer stack version ?](#using-a-newer-stack-version)

## Requirements

### Host setup

1. Install [Docker](https://www.docker.com/community-edition#/download)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)

## Usage

### Bringing up the stack

**Note**: Run `docker-compose build` first

Start the platform using `docker-compose`:

```console
$ docker-compose --compatibility up
```

You can also run all services in the background (detached mode) by adding the `-d` flag to the above command.

Give Kibana a few seconds to initialize, then access the Kibana web UI by hitting
[http://<CONTAINER_IP>:5601](http://CONTAINER_IP:5601) with a web browser.

By default, the platform exposes the following ports:
* 4369: epmd, a peer discovery service used by RabbitMQ nodes and CLI tools
* 5672, 5671: used by AMQP 0-9-1 and 1.0 clients without and with TLS
* 25672: used for inter-node and CLI tools communication (Erlang distribution server port) and is allocated from a dynamic range (limited to a single port by default, computed as AMQP port + 20000). Unless external connections on these ports are really necessary (e.g. the cluster uses federation or CLI tools are used on machines outside the subnet), these ports should not be publicly exposed. See networking guide for details.
* 35672-35682: used by CLI tools (Erlang distribution client ports) for communication with nodes and is allocated from a dynamic range (computed as server distribution port + 10000 through server distribution port + 10010). See networking guide for details.
* 15672: HTTP API clients, management UI and rabbitmqadmin (only if the management plugin is enabled)
* 61613, 61614: STOMP clients without and with TLS (only if the STOMP plugin is enabled)
* 1883, 8883: (MQTT clients without and with TLS, if the MQTT plugin is enabled
* 15674: STOMP-over-WebSockets clients (only if the Web STOMP plugin is enabled)
* 15675: MQTT-over-WebSockets clients (only if the Web MQTT plugin is enabled)
* 9200: Elasticsearch HTTP
* 9300: Elasticsearch TCP transport
* 5601: Kibana

## Configuration

**NOTE**: Configuration is not dynamically reloaded, you will need to restart the stack after any change in the
configuration of a component.

### How can I tune the Kibana configuration?

The Kibana default configuration is stored in `kibana/config/kibana.yml`.

It is also possible to map the entire `config` directory instead of a single file.

### How can I tune the Elasticsearch configuration?

The Elasticsearch configuration is stored in `elasticsearch/config/elasticsearch.yml`.

You can also specify the options you want to override directly via environment variables:

```yml
elasticsearch:

  environment:
    network.host: "_non_loopback_"
    cluster.name: "my-cluster"
```

### How can I scale out the Elasticsearch cluster?

Follow the instructions from the Wiki: [Scaling out
Elasticsearch](https://github.com/deviantony/docker-elk/wiki/Elasticsearch-cluster)

## Storage

### How can I persist Elasticsearch data?

The data stored in Elasticsearch will be persisted after container reboot but not after container removal.

In order to persist Elasticsearch data even after removing the Elasticsearch container, you'll have to mount a volume on
your Docker host. Update the `elasticsearch` service declaration to:

```yml
elasticsearch:

  volumes:
    - /path/to/storage:/usr/share/elasticsearch/data
```

This will store Elasticsearch data inside `/path/to/storage`.

**NOTE:** beware of these OS-specific considerations:
* **Linux:** the [unprivileged `elasticsearch` user][esuser] is used within the Elasticsearch image, therefore the
  mounted data directory must be owned by the uid `1000`.

[esuser]: https://github.com/elastic/elasticsearch-docker/blob/016bcc9db1dd97ecd0ff60c1290e7fa9142f8ddd/templates/Dockerfile.j2#L22


### Using a newer stack version

To use a different Elastic Stack version than the one currently available in the repository, simply change the version
number inside the `.env` file, and rebuild the platform with:

```console
$ docker-compose build
```

**NOTE**: Always pay attention to the [upgrade instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html)
for each individual component before performing a stack upgrade.

The information contained is for general information purposes only.
