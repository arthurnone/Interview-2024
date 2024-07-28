# Use the official Ruby base image
FROM ruby:latest

# Set environment variables
ENV RAILS_ENV=production \
    BUNDLE_PATH=/gems

# Install essential dependencies
RUN apt-get update -qq && apt-get install -y \
  build-essential \
  libpq-dev \
  libreadline-dev \
  sqlite3 \
  libsqlite3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY order-api /app
WORKDIR /app
RUN bundle install --no-deployment

WORKDIR /www
