#!/bin/bash

cat <<EOF >> fablo-target/fabric-docker/docker-compose.yaml
  nodeexporter:
    container_name: nodeexporter
    image: prom/node-exporter
    ports:
      - 9100:9100
    volumes:
      - /proc:/host/proc
      - /sys:/host/sys
      - /:/rootfs
    networks:
      - basic

  cadvisor:
    container_name: cadvisor
    image:  gcr.io/cadvisor/cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro 
      - /var/run:/var/run:ro 
      - /sys:/sys:ro 
      - /var/lib/docker/:/var/lib/docker:ro 
      - /dev/disk/:/dev/disk:ro 
    networks:
      - basic    

  prometheus:
    container_name: prometheus
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ../../prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - basic

  grafana:
    container_name: grafana
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ../../../fabric-benchmarks/caliper/prometheus/grafana/grafana:/var/lib/grafana
      - ../../../fabric-benchmarks/caliper/prometheus/grafana/conf:/usr/share/grafana/conf
    user: "\$UID:\$GID" # this has to be id of a user able to write to /usr. 
    networks:
      - basic

  pushGateway:
    image: prom/pushgateway
    container_name: pushGateway
    ports:
      - "9091:9091"
    networks:
      - basic
EOF
