#!/bin/bash

CGO_ENABLED=1 GOARCH=arm64 GOOS=darwin go build -buildmode=c-shared -o bridge.so bridge.go