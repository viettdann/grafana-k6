#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Fetch the latest release information
LATEST_RELEASE=$(curl -s https://api.github.com/repos/grafana/k6/releases/latest)

# Extract the tag name (version)
if command_exists jq; then
    VERSION=$(echo "$LATEST_RELEASE" | jq -r .tag_name)
else
    VERSION=$(echo "$LATEST_RELEASE" | grep -o '"tag_name": *"[^"]*"' | sed 's/.*: *"\(.*\)"/\1/')
fi

# Determine system architecture and OS
ARCH=$(uname -m)
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Map architecture names
case $ARCH in
    x86_64)
        ARCH="amd64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# Create bin directory if it doesn't exist
mkdir -p ./bin

# Determine file extension and OS-specific settings
case $OS in
    linux)
        EXT="tar.gz"
        OS_NAME="linux"
        ;;
    darwin)
        EXT="zip"
        OS_NAME="macos"
        ;;
    *)
        echo "Unsupported operating system: $OS"
        exit 1
        ;;
esac

# Construct the filename
FILENAME="k6-${VERSION}-${OS_NAME}-${ARCH}.${EXT}"
K6_FILE="k6-${VERSION}-${OS_NAME}-${ARCH}"

# Extract the download URL for the appropriate file
if command_exists jq; then
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE" | jq -r ".assets[] | select(.name == \"$FILENAME\") | .browser_download_url")
else
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE" | grep -o '"browser_download_url": *"[^"]*'${FILENAME}'"' | sed 's/.*: *"\(.*\)"/\1/')
fi

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Could not find download URL for $FILENAME"
    exit 1
fi

# Download the file
echo "Downloading $FILENAME..."
curl -L -o "$FILENAME" "$DOWNLOAD_URL"

echo "Download complete: $FILENAME"

# Extract the binary
echo "Extracting k6 binary..."
case $OS in
    linux)
        echo "Linux"
        tar -xzf "$FILENAME"
        mv "$K6_FILE/k6" ./bin/k6
        ;;
    darwin)
        echo "macOS"
        unzip "$FILENAME"
        mv "$K6_FILE/k6" ./bin/k6
        ;;
esac

Clean up
rm -rf "$FILENAME" "$K6_FILE"

# Check if k6 binary was successfully extracted
if [ ! -f ./bin/k6 ]; then
    echo "Error: Failed to extract k6 binary"
    exit 1
fi

echo "k6 binary successfully installed to ./bin/k6"