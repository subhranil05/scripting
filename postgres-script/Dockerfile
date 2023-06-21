FROM alpine:latest

# Install PostgreSQL client
RUN apk add --no-cache postgresql-client

# Copy the script to the container
ADD script.sh /usr/local/bin

# Set soft link
RUN chmod +x /usr/local/bin/script.sh && ln -s /usr/local/bin/script.sh /postgres_script

# Run the script
ENTRYPOINT ["/bin/sh", "-c", "trap : TERM INT; sleep infinity & wait"]
