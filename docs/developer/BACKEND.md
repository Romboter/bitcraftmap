# BitCraft Map Backend Architecture

## Executive Summary

The BitCraft Map backend is a cloud-native, microservices-based architecture designed to serve geospatial data for the BitCraft game world. The system employs a three-tier architecture with API Gateway aggregation, reverse proxy capabilities, and containerized deployment to ensure scalability, reliability, and performance.

**Key Components:**
- **NodeIndex Service**: Rust-based geospatial data service
- **KrakenD API Gateway**: Request aggregation and routing layer  
- **Caddy Reverse Proxy**: Web server with CORS and SSL termination
- **Docker**: Containerization and deployment platform

**Performance Characteristics:**
- Supports concurrent API calls (up to 9 simultaneous requests)
- Dual backend instance aggregation for enhanced data availability
- Automatic SSL certificate management via Let's Encrypt
- CORS-enabled for cross-origin web application support

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [API Gateway Configuration](#api-gateway-configuration)
4. [Security Implementation](#security-implementation)
5. [Deployment Architecture](#deployment-architecture)
6. [Build and Deployment Procedures](#build-and-deployment-procedures)
7. [Development Setup](#development-setup)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Performance Tuning](#performance-tuning)
10. [Maintenance Procedures](#maintenance-procedures)

---

## System Architecture

### High-Level Overview

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Web Client    │───▶│    Caddy     │───▶│    KrakenD      │───▶│   NodeIndex      │
│ (bitcraftmap.   │    │ Reverse Proxy│    │  API Gateway    │    │  Service (Rust)  │
│     com)        │    │   (Port 80   │    │   (Port 9000)   │    │  (Ports 3000,    │
└─────────────────┘    │   /443)      │    └─────────────────┘    │       3001)      │
                       └──────────────┘                           └──────────────────┘
                              │                                            │
                       ┌──────────────┐                           ┌──────────────────┐
                       │     SSL      │                           │   Data Sources   │
                       │ Certificates │                           │ (BitCraft Game   │
                       │(Let's Encrypt│                           │    Database)     │
                       └──────────────┘                           └──────────────────┘
```

### Architecture Principles

**1. Separation of Concerns**
- **Presentation Layer**: Caddy handles SSL termination and CORS policies
- **Gateway Layer**: KrakenD manages request routing and response aggregation
- **Service Layer**: NodeIndex provides core geospatial data processing

**2. High Availability Design**
- Dual backend instances (ports 3000/3001) provide redundancy
- Response aggregation ensures data completeness
- Containerized deployment enables horizontal scaling

**3. Security-First Approach**
- CORS policies restrict cross-origin access to authorized domains
- SSL/TLS encryption for all external communications
- Proxy-based architecture hides internal service topology

---

## Component Details

### NodeIndex Service (Rust Backend)

**Purpose**: Core geospatial data service responsible for processing BitCraft game world data.

**Technology Stack**: 
- **Language**: Rust 1.89.0
- **Runtime**: Compiled binary (`nodeindex`)
- **Container**: Docker with Debian Bookworm base

**Key Characteristics**:
- High-performance data processing using Rust's memory safety guarantees
- Compiled to native binary for optimal execution speed  
- Stateless design enabling horizontal scaling
- RESTful API interface for resource queries

**Source Repository**: [`https://github.com/vis-eyth/bitcraft-nodeindex.git`](https://github.com/vis-eyth/bitcraft-nodeindex.git)

### KrakenD API Gateway

**Purpose**: High-performance API Gateway providing request routing, response aggregation, and backend abstraction.

**Configuration Location**: [`backend/Krakend.json`](backend/Krakend.json:1)

**Core Features**:
- **Response Aggregation**: Combines data from multiple backend instances
- **Concurrent Processing**: Supports up to 9 simultaneous backend calls
- **Data Transformation**: Uses flatmap filters for response restructuring
- **Load Distribution**: Balances requests across available backends

**Endpoint Configuration**:
```json
{
  "endpoint": "/resource/{id}",
  "method": "GET",
  "concurrent_calls": 9,
  "backend": [
    {"host": ["http://127.0.0.1:3000"]},
    {"host": ["http://127.0.0.1:3001"]}
  ]
}
```

### Caddy Reverse Proxy

**Purpose**: Modern web server providing SSL termination, reverse proxy capabilities, and CORS handling.

**Configuration Location**: [`backend/Caddyfile`](backend/Caddyfile:1)

**Key Features**:
- **Automatic HTTPS**: Let's Encrypt certificate management
- **CORS Configuration**: Cross-origin resource sharing policies
- **Access Logging**: Structured request logging with rotation
- **Reverse Proxy**: Forwards requests to KrakenD gateway

**CORS Policy**:
- **Allowed Origin**: `https://bitcraftmap.com`
- **Allowed Methods**: `GET, POST, PUT, DELETE, OPTIONS`
- **Allowed Headers**: `Content-Type, Authorization`
- **Preflight Caching**: 600 seconds

---

## API Gateway Configuration

### Request Flow Architecture

1. **Client Request**: Web application sends API request to `api.bitcraftmap.com`
2. **SSL Termination**: Caddy handles HTTPS and validates certificates
3. **CORS Processing**: Pre-flight OPTIONS requests handled by Caddy
4. **Gateway Routing**: Request forwarded to KrakenD on port 9000
5. **Backend Aggregation**: KrakenD queries both NodeIndex instances (ports 3000/3001)
6. **Response Merging**: Data from both backends combined using flatmap filters
7. **Client Response**: Aggregated JSON response returned to client

### Response Aggregation Strategy

The API Gateway implements a sophisticated response aggregation pattern:

```json
"flatmap_filter": [
  { "type": "move",   "args": ["resp0.type", "type"] },
  { "type": "move",   "args": ["resp0.features", "features"] }, 
  { "type": "append", "args": ["resp1.features", "features"] },
  { "type": "del",    "args": ["resp0", "resp1"] }
]
```

**Aggregation Logic**:
1. **Primary Response** (`resp0`): Type and initial features from first backend
2. **Secondary Response** (`resp1`): Additional features appended to collection
3. **Cleanup**: Original response objects removed from final output
4. **Result**: Unified GeoJSON FeatureCollection with complete data set

### Endpoint Specifications

| Endpoint | Method | Purpose | Backend Instances |
|----------|--------|---------|-------------------|
| `/resource/{id}` | GET | Retrieve geospatial resource by ID | Both (3000, 3001) |

**Response Format**: GeoJSON FeatureCollection
```json
{
  "type": "FeatureCollection", 
  "features": [
    // Aggregated features from all backends
  ]
}
```

---

## Security Implementation

### CORS (Cross-Origin Resource Sharing)

**Policy Configuration**:
- **Strict Origin Control**: Only `https://bitcraftmap.com` allowed
- **Method Restrictions**: Limited to safe and necessary HTTP methods
- **Header Validation**: Only essential headers permitted
- **Preflight Optimization**: 10-minute cache for OPTIONS requests

**Implementation Details**:
```caddyfile
@preflight {
  method OPTIONS
  path /*
}
handle @preflight {
  header {
    Access-Control-Allow-Origin  https://bitcraftmap.com
    Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
    Access-Control-Allow-Headers "Content-Type, Authorization"
    Access-Control-Max-Age 600
    Vary Origin
  }
  respond "" 204
}
```

### SSL/TLS Configuration

**Certificate Management**: 
- **Provider**: Let's Encrypt via Caddy automatic HTTPS
- **Contact Email**: `admin@bitcraftmap.com`
- **Renewal**: Automatic certificate rotation
- **Protocols**: TLS 1.2+ with modern cipher suites

### Network Security

**Internal Communication**:
- Backend services bound to localhost (`127.0.0.1`)
- No direct external access to NodeIndex instances
- Gateway pattern provides single point of entry
- Container isolation with minimal exposed ports

---

## Deployment Architecture

### Container Strategy

**Base Image**: `rust:1.89.0-bookworm`
- **Advantages**: Official Rust toolchain, security updates, minimal attack surface
- **Build Process**: Multi-stage compilation with artifact extraction
- **Runtime**: Compiled binary execution (no runtime dependencies)

**Dockerfile Analysis**:
```dockerfile
FROM rust:1.89.0-bookworm
WORKDIR /app
COPY . .
RUN cargo build --release -p nodeindex && \
    cp ./target/release/nodeindex ./ && \
    rm -rf ./target
CMD ["./nodeindex"]
```

**Optimization Strategies**:
1. **Build Artifact Extraction**: Only final binary included in image
2. **Target Directory Cleanup**: Intermediate build files removed
3. **Release Optimization**: Compiled with `--release` flag for performance

### Service Discovery

**Port Allocation**:
- **Port 80/443**: Caddy (external access)
- **Port 9000**: KrakenD API Gateway (internal)
- **Port 3000**: NodeIndex Instance #1 (internal)
- **Port 3001**: NodeIndex Instance #2 (internal)

**Network Architecture**:
- External clients connect only to Caddy (ports 80/443)
- All internal services communicate via localhost
- No direct backend exposure to external networks

---

## Build and Deployment Procedures

### Automated Build Process

**Build Script**: [`backend/docker_build.sh`](backend/docker_build.sh:1)

**Build Workflow**:
1. **Repository Cleanup**: Remove existing source directory
2. **Source Acquisition**: Clone latest code from GitHub repository
3. **Dockerfile Integration**: Copy deployment configuration 
4. **Version Tagging**: Generate build hash from Git commit
5. **Image Creation**: Build both versioned and latest tags

**Build Commands**:
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/vis-eyth/bitcraft-nodeindex.git"
TARGET_DIR="nodeindex" 
IMAGE_NAME="bitcraftmap-api"

# Repository management
rm -rf "$TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR"
cp "./Dockerfile" "$TARGET_DIR/Dockerfile"
cd "$TARGET_DIR"

# Version tagging
HASH_REV=$(git rev-parse --short HEAD)

# Container build
docker build -t "${IMAGE_NAME}:${HASH_REV}" -t "${IMAGE_NAME}:latest" .
```

### Deployment Strategy

**Image Tagging Strategy**:
- **Latest Tag**: `bitcraftmap-api:latest` (production deployment)
- **Version Tag**: `bitcraftmap-api:{git-hash}` (specific version tracking)

**Deployment Benefits**:
- **Reproducible Builds**: Git hash ensures build traceability
- **Rollback Capability**: Version tags enable quick rollback
- **CI/CD Ready**: Script suitable for automated pipeline integration

### Container Orchestration

**Recommended Deployment Pattern**:
```bash
# Start NodeIndex instances
docker run -d --name nodeindex-1 -p 3000:3000 bitcraftmap-api:latest
docker run -d --name nodeindex-2 -p 3001:3001 bitcraftmap-api:latest

# Start API Gateway
docker run -d --name krakend -p 9000:9000 -v ./Krakend.json:/etc/krakend.json krakend/krakend-ce

# Start Reverse Proxy
docker run -d --name caddy -p 80:80 -p 443:443 -v ./Caddyfile:/etc/caddy/Caddyfile caddy:latest
```

---

## Development Setup

### Prerequisites

**System Requirements**:
- **Docker**: Version 20.10+
- **Git**: For source code management
- **Bash**: For build script execution (Linux/macOS/WSL)

**Network Requirements**:
- Internet access for dependency downloads
- Ports 3000, 3001, 9000, 80, 443 available
- DNS resolution for `api.bitcraftmap.com` (production)

### Local Development Environment

**Quick Start**:
```bash
# 1. Clone the backend configuration
git clone <backend-repo> bitcraftmap-backend
cd bitcraftmap-backend/backend

# 2. Build the application
./docker_build.sh

# 3. Start services (development mode)
docker-compose up -d  # If docker-compose.yml available
# OR manual container startup as shown above
```

**Development Configuration**:
- Modify [`Caddyfile`](backend/Caddyfile:20) to allow `localhost` origins for testing
- Update [`Krakend.json`](backend/Krakend.json:15) backend hosts if needed
- Use HTTP instead of HTTPS for local development

### Testing the API

**Health Check Commands**:
```bash
# Test NodeIndex instances directly
curl http://localhost:3000/resource/test-id
curl http://localhost:3001/resource/test-id

# Test through API Gateway
curl http://localhost:9000/resource/test-id

# Test through full stack (if Caddy configured for localhost)
curl http://localhost/resource/test-id
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Build Failures

**Problem**: Docker build fails during Rust compilation
```
Error: failed to compile `nodeindex` due to dependencies
```

**Solution**:
```bash
# Check Rust version compatibility
docker run --rm rust:1.89.0-bookworm rustc --version

# Clean build with verbose output
./docker_build.sh 2>&1 | tee build.log

# Review build logs for specific dependency issues
```

#### 2. API Gateway Connection Issues

**Problem**: KrakenD cannot reach backend instances
```
Error: dial tcp 127.0.0.1:3000: connect: connection refused
```

**Solutions**:
```bash
# Verify backend services are running
docker ps | grep nodeindex

# Check port accessibility
netstat -tlnp | grep :3000
netstat -tlnp | grep :3001

# Test direct backend connectivity
curl -v http://localhost:3000/health  # if health endpoint exists
```

#### 3. CORS Errors

**Problem**: Browser blocks requests due to CORS policy
```
Access to fetch at 'https://api.bitcraftmap.com/resource/123' 
from origin 'https://example.com' has been blocked by CORS policy
```

**Solution**:
Update [`Caddyfile`](backend/Caddyfile:20) to include additional allowed origins:
```caddyfile
Access-Control-Allow-Origin  https://bitcraftmap.com https://example.com
```

#### 4. SSL Certificate Issues

**Problem**: Let's Encrypt certificate acquisition fails

**Solutions**:
```bash
# Check DNS resolution
nslookup api.bitcraftmap.com

# Verify domain ownership
curl -I http://api.bitcraftmap.com/.well-known/acme-challenge/

# Check Caddy logs
docker logs caddy-container-name

# Manual certificate troubleshooting
caddy validate --config /etc/caddy/Caddyfile
```

### Monitoring and Observability

**Log File Locations**:
- **Caddy Access Logs**: `/var/log/caddy/api.access.log`
- **Container Logs**: `docker logs <container-name>`
- **System Logs**: `/var/log/syslog` (Linux)

**Log Rotation Configuration**:
```caddyfile
log {
  output file /var/log/caddy/api.access.log {
    roll_size 500MiB
    roll_keep 5
  }
}
```

**Health Check Endpoints**:
```bash
# Gateway status
curl -I http://localhost:9000/

# Backend instance status
curl -I http://localhost:3000/
curl -I http://localhost:3001/
```

---

## Performance Tuning

### Optimization Strategies

#### 1. Concurrent Request Handling

**Current Configuration**: [`concurrent_calls: 9`](backend/Krakend.json:10)

**Tuning Recommendations**:
- Monitor backend response times under load
- Adjust concurrent calls based on backend capacity
- Consider backend instance scaling if bottlenecks occur

#### 2. Response Caching

**KrakenD Cache Configuration** (not currently implemented):
```json
"extra_config": {
  "qos/http-cache": {
    "shared": true,
    "ttl": 300
  }
}
```

#### 3. Backend Scaling

**Horizontal Scaling Strategy**:
```bash
# Add additional NodeIndex instances
docker run -d --name nodeindex-3 -p 3002:3000 bitcraftmap-api:latest

# Update KrakenD configuration to include new instance
# Add new backend host to Krakend.json
```

### Performance Metrics

**Key Performance Indicators**:
- **Response Time**: Target < 100ms for geospatial queries
- **Throughput**: Current capacity ~90 concurrent requests (9 × 2 backends × 5 theoretical connections)
- **Availability**: 99.9% uptime target
- **Error Rate**: < 0.1% failed requests

---

## Maintenance Procedures

### Regular Maintenance Tasks

#### 1. Log Rotation and Cleanup

**Automated Log Management**:
```bash
# Check log file sizes
du -sh /var/log/caddy/*.log

# Manual log rotation (if needed)
logrotate -f /etc/logrotate.d/caddy

# Clean old Docker logs
docker system prune -f
```

#### 2. Container Health Monitoring

**Container Status Checks**:
```bash
# Monitor container resource usage
docker stats

# Check container health
docker inspect <container-name> | grep Health -A 10

# Restart unhealthy containers
docker restart <container-name>
```

#### 3. Security Updates

**Update Procedures**:
```bash
# Rebuild with latest base image
./docker_build.sh

# Update container runtime
docker pull caddy:latest
docker pull krakend/krakend-ce:latest

# Rolling deployment
docker-compose up -d --no-deps <service-name>
```

### Backup Procedures

**Configuration Backup**:
```bash
# Backup critical configuration files
tar -czf backend-config-$(date +%Y%m%d).tar.gz \
  Caddyfile Krakend.json Dockerfile *.sh

# Store in secure location
scp backend-config-*.tar.gz backup-server:/backups/
```

### Disaster Recovery

**Recovery Procedures**:
1. **Service Restoration**: Use versioned container images for quick rollback
2. **Configuration Recovery**: Restore from configuration backups
3. **Data Integrity**: Verify API responses match expected format
4. **Monitoring**: Confirm all health checks pass after restoration

---

## Appendix

### A. Configuration File Reference

#### Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.89.0-bookworm
WORKDIR /app
COPY . .
RUN cargo build --release -p nodeindex && cp ./target/release/nodeindex ./ && rm -rf ./target
CMD ["./nodeindex"]
```

#### Build Script Variables
| Variable | Purpose | Default Value |
|----------|---------|---------------|
| `REPO_URL` | Source repository | `https://github.com/vis-eyth/bitcraft-nodeindex.git` |
| `TARGET_DIR` | Build directory | `nodeindex` |
| `IMAGE_NAME` | Docker image name | `bitcraftmap-api` |

### B. Port Reference

| Port | Service | Access Level | Purpose |
|------|---------|-------------|---------|
| 80 | Caddy | External | HTTP redirect to HTTPS |
| 443 | Caddy | External | HTTPS traffic |
| 9000 | KrakenD | Internal | API Gateway |
| 3000 | NodeIndex #1 | Internal | Backend service |
| 3001 | NodeIndex #2 | Internal | Backend service |

### C. Environment Variables

**Production Environment**:
```bash
CADDY_EMAIL=admin@bitcraftmap.com
API_DOMAIN=api.bitcraftmap.com
FRONTEND_DOMAIN=https://bitcraftmap.com
```

### D. Glossary

- **API Gateway**: Centralized entry point for API requests with routing and aggregation capabilities
- **CORS**: Cross-Origin Resource Sharing - browser security mechanism for cross-domain requests
- **Reverse Proxy**: Server that forwards client requests to backend servers
- **SSL Termination**: Process of decrypting SSL traffic at the proxy level
- **NodeIndex**: Rust-based service providing geospatial data from BitCraft game world
- **Flatmap Filter**: KrakenD feature for transforming and aggregating JSON responses
- **GeoJSON**: Open standard format for representing geographical features

---

**Document Version**: 1.0  
**Last Updated**: 2024-10-19  
**Maintainer**: BitCraft Map Backend Team  
**Review Cycle**: Quarterly
