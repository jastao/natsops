# syntax=docker/dockerfile:1

ARG BUILD_IMAGE=localhost:8083/maven:3.8.6-eclipse-temurin-17
FROM ${BUILD_IMAGE} AS setup

ARG MAVEN_OPT=-Dmaven.wagon.http.ssl.insecure=true

WORKDIR /app

ADD settings.xml settings-security.xml /root/.m2/
COPY pom.xml .
COPY src ./src

FROM setup AS build

RUN mvn clean install ${MAVEN_OPT}

FROM setup AS deploy

RUN mvn clean deploy ${MAVEN_OPT}

