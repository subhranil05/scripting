FROM alpine:latest

# Install PostgreSQL client
RUN apk add --no-cache postgresql-client

# Copy the script to the container
ADD install-ext.sh migration-script.sh /usr/local/bin/

# Set soft link
RUN chmod +x /usr/local/bin/install-ext.sh /usr/local/bin/migration-script.sh && \
    ln -s /usr/local/bin/install-ext.sh /install-ext && \
    ln -s /usr/local/bin/migration-script.sh /migration

# Run the script
ENTRYPOINT ["/bin/sh", "-c", "trap : TERM INT; sleep infinity & wait"]
