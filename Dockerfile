FROM python:3.11

# Set destination for COPY
WORKDIR /app

# Copy repo
COPY ../.. ./

# Build
RUN make install
