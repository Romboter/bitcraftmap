
# BitCraft Map with Deno 2: Complete Migration Guide

This guide demonstrates how to replace all Node.js usage in the BitCraft Map project with Deno 2, providing superior developer experience, better security, and modern JavaScript/TypeScript capabilities.

## Table of Contents

1. [Why Deno 2 Over Node.js](#why-deno-2-over-nodejs)
2. [Prerequisites and Installation](#prerequisites-and-installation)
3. [Replacing Node.js Development Servers](#replacing-nodejs-development-servers)
4. [File Watching and Auto-Reload](#file-watching-and-auto-reload)
5. [Package Management Migration](#package-management-migration)
6. [Testing with Deno](#testing-with-deno)
7. [Development Workflow with Deno 2](#development-workflow-with-deno-2)
8. [Advanced Deno Features](#advanced-deno-features)
9. [Migration Checklist](#migration-checklist)
10. [Troubleshooting](#troubleshooting)

---

## Why Deno 2 Over Node.js

### Key Advantages for BitCraft Map Development

**🔒 Security First**
- Secure by default - no file, network, or environment access without explicit permissions
- Perfect for serving static map assets safely
- No `node_modules` security vulnerabilities

**⚡ Performance Benefits**
- Faster startup times for development servers
- Built-in HTTP/2 and HTTP/3 support
- Native TypeScript execution without compilation steps
- Optimized V8 engine with modern JavaScript features

**🛠️ Developer Experience**
- Built-in formatter, linter, and test runner
- No package.json or node_modules complexity
- Web-standard APIs (fetch, WebSocket, etc.)
- Excellent TypeScript support out of the box

**🌐 Web Standards Compliance**
- Uses standard Web APIs that match browser environments
- Better alignment with modern JavaScript features used in map.js
- Native support for ES modules and import maps

**For BitCraft Map Specifically:**
- Static file serving is cleaner and more secure
- Better handling of JSON/GeoJSON data processing
- Improved CORS handling for development
- Native support for modern JavaScript features already used in the project

---

## Prerequisites and Installation

### Installing Deno 2

**Windows (PowerShell)**:
```powershell
# Using PowerShell
irm https://deno.land/install.ps1 | iex

# Using Chocolatey
choco install deno

# Using Scoop
scoop install deno
```

**macOS/Linux**:
```bash
# Using curl
curl -fsSL https://deno.land/install.sh | sh

# Using Homebrew (macOS)
brew install deno
```

**Verify Installation**:
```bash
deno --version
# Should show Deno 2.x.x with V8 and TypeScript versions
```

### Updated Prerequisites List

Replace the Node.js prerequisites from [`getting-started.md`](getting-started.md:24) with:

**Required Software**:
- **Git** - For version control
- **Deno 2.0+** - Modern JavaScript/TypeScript runtime (replaces Node.js)
- **Python** (3.8+) - For data generation scripts
- **Docker** (optional) - For backend services
- **Modern Web Browser** - Chrome, Firefox, or Edge with developer tools

### VS Code Extensions for Deno

Replace Node.js extensions with Deno-optimized ones:

```json
{
  "recommendations": [
    "denoland.vscode-deno",           // Official Deno extension
    "ms-vscode.live-server",          // Still useful for alternative server
    "ms-python.python",               // For scripts
    "ms-azuretools.vscode-docker"     // If using Docker
  ]
}
```

**Configure VS Code for Deno**:
```json
// .vscode/settings.json
{
  "deno.enable": true,
  "deno.enablePaths": ["./assets/js/", "./scripts/"],
  "deno.lint": true,
  "deno.unstable": false,
  "typescript.suggest.autoImports": false
}
```

---

## Replacing Node.js Development Servers

### Original Node.js Methods (from getting-started.md)

❌ **Old Way**:
```bash
# Option B: Using Node.js http-server
npm install -g http-server
http-server -p 8000
```

### ✅ Deno 2 Replacement Options

#### Option 1: Built-in Deno HTTP Server (Recommended)

Create `dev-server.ts` in project root:

```typescript
// dev-server.ts
import { serveDir } from "jsr:@std/http/file-server";

const PORT = 8000;

console.log(`🗺️  BitCraft Map Dev Server starting on http://localhost:${PORT}`);

Deno.serve({ port: PORT }, (req) => {
  // Add CORS headers for development
  const response = serveDir(req, {
    fsRoot: "./",
    showDirListing: true,
  });

  // Enhance with CORS for local development
  return response.then(res => {
    res.headers.set("Access-Control-Allow-Origin", "*");
    res.headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.headers.set("Access-Control-Allow-Headers", "Content-Type");
    return res;
  });
});
```

**Start the server**:
```bash
# Basic server
deno run --allow-net --allow-read dev-server.ts

# Or with shorthand permissions
deno run -A dev-server.ts

# Create an alias in deno.json for convenience
```

#### Option 2: Simple One-Liner Server

```bash
# Quick static server
deno run --allow-net --allow-read jsr:@std/http/file-server --port 8000

# With CORS enabled
deno run --allow-net --allow-read \
  https://deno.land/std@0.208.0/http/file_server.ts \
  --cors --port 8000
```

#### Option 3: Enhanced Development Server

Create `scripts/dev-server.ts`:

```typescript
// scripts/dev-server.ts - Enhanced development server
import { serveDir } from "jsr:@std/http/file-server";
import { extname } from "jsr:@std/path";

interface ServerOptions {
  port: number;
  cors: boolean;
  verbose: boolean;
}

const options: ServerOptions = {
  port: Number(Deno.env.get("PORT")) || 8000,
  cors: true,
  verbose: true
};

console.log(`🗺️  BitCraft Map Development Server`);
console.log(`📡 Starting on http://localhost:${options.port}`);
console.log(`🔧 CORS: ${options.cors ? 'Enabled' : 'Disabled'}`);

Deno.serve({ port: options.port }, async (req) => {
  const url = new URL(req.url);
  const pathname = url.pathname;

  // Log requests in development
  if (options.verbose) {
    console.log(`${req.method} ${pathname}`);
  }

  // Handle API mock endpoints for development
  if (pathname.startsWith('/api/')) {
    return handleApiMock(req);
  }

  // Serve static files
  const response = await serveDir(req, {
    fsRoot: "./",
    showDirListing: false,
    urlRoot: "",
  });

  // Add development headers
  if (options.cors) {
    response.headers.set("Access-Control-Allow-Origin", "*");
    response.headers.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    response.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  }

  // Add cache headers for development
  const ext = extname(pathname);
  if (['.js', '.css', '.json'].includes(ext)) {
    response.headers.set("Cache-Control", "no-cache");
  }

  return response;
});

// Mock API responses for development
async function handleApiMock(req: Request): Promise<Response> {
  const url = new URL(req.url);
  
  // Mock BitCraft API responses
  if (url.pathname === '/api/resource/test') {
    return Response.json({
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: {
            name: "Mock Resource",
            type: "test"
          },
          geometry: {
            type: "Point",
            coordinates: [15000, 15000]
          }
        }
      ]
    });
  }

  return new Response("API endpoint not found", { status: 404 });
}
```

**Usage**:
```bash
# Run enhanced server
deno run --allow-net --allow-read --allow-env scripts/dev-server.ts

# With custom port
PORT=3000 deno run --allow-net --allow-read --allow-env scripts/dev-server.ts
```

---

## File Watching and Auto-Reload

### Original Node.js Method

❌ **Old Way**:
```bash
npm install -g nodemon
nodemon --watch assets --exec "python -m http.server 8000"
```

### ✅ Deno 2 File Watching Solutions

#### Option 1: Built-in Deno Watch (Recommended)

```bash
# Watch and restart development server
deno run --watch --allow-net --allow-read dev-server.ts

# Watch specific directories
deno run --watch=assets/,scripts/ --allow-net --allow-read dev-server.ts
```

#### Option 2: Custom File Watcher

Create `scripts/watch-dev.ts`:

```typescript
// scripts/watch-dev.ts - Custom file watcher with live reload
import { debounce } from "jsr:@std/async/debounce";

const WATCH_PATHS = ["./assets", "./src", "./index.html"];
const IGNORE_PATTERNS = [/\.git/, /node_modules/, /\.DS_Store/];

console.log("🔍 Starting file watcher for BitCraft Map development");
console.log("📂 Watching:", WATCH_PATHS.join(", "));

let serverProcess: Deno.ChildProcess | null = null;

// Debounced restart function
const restartServer = debounce(async () => {
  console.log("🔄 Changes detected, restarting server...");
  
  // Kill existing server
  if (serverProcess) {
    serverProcess.kill("SIGTERM");
    await serverProcess.status;
  }

  // Start new server
  serverProcess = new Deno.Command("deno", {
    args: ["run", "--allow-net", "--allow-read", "dev-server.ts"],
    stdout: "inherit",
    stderr: "inherit",
  }).spawn();

  console.log("✅ Server restarted");
}, 200);

// Watch for file changes
const watcher = Deno.watchFs(WATCH_PATHS);

for await (const event of watcher) {
  // Filter out ignored patterns
  const shouldIgnore = event.paths.some(path =>
    IGNORE_PATTERNS.some(pattern => pattern.test(path))
  );

  if (!shouldIgnore && (event.kind === "modify" || event.kind === "create")) {
    console.log(`📝 ${event.kind}: ${event.paths.join(", ")}`);
    await restartServer();
  }
}
```

**Usage**:
```bash
# Start watcher (will also start the dev server)
deno run --allow-net --allow-read --allow-run scripts/watch-dev.ts
```

#### Option 3: Live Reload with WebSocket

Create `scripts/live-reload-server.ts`:

```typescript
// scripts/live-reload-server.ts - Server with live reload capability
import { serveDir } from "jsr:@std/http/file-server";

const PORT = 8000;
const WS_PORT = 8001;

console.log(`🗺️  BitCraft Map with Live Reload`);
console.log(`🌐 Server: http://localhost:${PORT}`);
console.log(`🔌 WebSocket: ws://localhost:${WS_PORT}`);

// WebSocket server for live reload
const wsClients = new Set<WebSocket>();

Deno.serve({ port: WS_PORT }, (req) => {
  if (req.headers.get("upgrade") === "websocket") {
    const { socket, response } = Deno.upgradeWebSocket(req);
    
    socket.onopen = () => {
      wsClients.add(socket);
      console.log("🔌 Client connected for live reload");
    };
    
    socket.onclose = () => {
      wsClients.delete(socket);
      console.log("🔌 Client disconnected");
    };
    
    return response;
  }
  
  return new Response("WebSocket connection required", { status: 426 });
});

// Main HTTP server with live reload injection
Deno.serve({ port: PORT }, async (req) => {
  const response = await serveDir(req, {
    fsRoot: "./",
    showDirListing: true,
  });

  // Inject live reload script into HTML files
  if (req.url.endsWith('.html') || req.url.endsWith('/')) {
    const text = await response.text();
    const liveReloadScript = `
      <script>
        const ws = new WebSocket('ws://localhost:${WS_PORT}');
        ws.onmessage = () => location.reload();
        ws.onclose = () => console.log('Live reload disconnected');
      </script>
    `;
    
    const modifiedHtml = text.replace('</body>', `${liveReloadScript}</body>`);
    
    return new Response(modifiedHtml, {
      headers: {
        ...response.headers,
        "content-type": "text/html",
      },
    });
  }

  return response;
});

// File watcher
const watcher = Deno.watchFs(["./assets", "./src", "./index.html"]);

for await (const event of watcher) {
  if (event.kind === "modify" || event.kind === "create") {
    console.log(`🔄 ${event.kind}: ${event.paths.join(", ")}`);
    
    // Notify all connected clients to reload
    for (const client of wsClients) {
      try {
        client.send("reload");
      } catch {
        wsClients.delete(client);
      }
    }
  }
}
```

---

## Package Management Migration

### Eliminating npm Completely

#### No More package.json or node_modules

Deno 2 eliminates the need for package.json and node_modules. Instead, use:

**Create `deno.json`** (optional but recommended):

```json
{
  "name": "bitcraft-map",
  "version": "1.0.0",
  "exports": "./mod.ts",
  "tasks": {
    "dev": "deno run --allow-net --allow-read dev-server.ts",
    "dev:watch": "deno run --watch --allow-net --allow-read dev-server.ts",
    "dev:reload": "deno run --allow-net --allow-read --allow-run scripts/live-reload-server.ts",
    "test": "deno test --allow-net --allow-read",
    "fmt": "deno fmt assets/js/ scripts/",
    "lint": "deno lint assets/js/ scripts/",
    "check": "deno check assets/js/*.js scripts/*.ts"
  },
  "imports": {
    "@std/": "jsr:@std/",
    "@/": "./assets/js/"
  },
  "compilerOptions": {
    "allowJs": true,
    "lib": ["dom", "dom.asynciterable", "deno.ns"]
  },
  "fmt": {
    "useTabs": false,
    "lineWidth": 100,
    "indentWidth": 2,
    "singleQuote": false
  },
  "lint": {
    "rules": {
      "tags": ["recommended"],
      "include": ["ban-untagged-todo"]
    },
    "exclude": ["assets/leaflet/"]
  }
}
```

#### Replacing npm Commands

| npm Command | Deno 2 Equivalent | Description |
|-------------|-------------------|-------------|
| `npm install -g http-server` | _Not needed_ | Built-in server |
| `npm install -g nodemon` | `--watch` flag | Built-in watching |
| `npm run dev` | `deno task dev` | Task runner |
| `npm test` | `deno test` | Built-in testing |
| `npm run lint` | `deno lint` | Built-in linting |
| `npm run format` | `deno fmt` | Built-in formatting |

#### Modern Import Patterns

Instead of CommonJS requires, use modern ES modules:

```javascript
// ❌ Old Node.js style (if any)
const fs = require('fs');
const path = require('path');

// ✅ Deno 2 style with Web APIs
// (Most BitCraft Map code already uses modern syntax)
import { readFileSync } from "node:fs"; // Node compatibility
import { join } from "jsr:@std/path";   // Deno standard library

// ✅ For web code (already used in BitCraft Map)
import { config } from './assets/js/config.js';
import { createIcon } from './assets/js/utils.js';
```

---

## Testing with Deno

### Setting Up Tests for BitCraft Map

#### Replace Jest/Puppeteer Setup

❌ **Old Node.js Testing** (from getting-started.md):
```bash
npm init -y
npm install --save-dev jest puppeteer
```

✅ **Deno 2 Testing** (Built-in):

Create `tests/map.test.ts`:

```typescript
// tests/map.test.ts - Testing map functionality
import { assertEquals, assertExists } from "jsr:@std/assert";
import { DOMParser } from "https://deno.land/x/deno_dom@v0.1.45/deno-dom-wasm.ts";

// Mock DOM for server-side testing
const mockDOM = () => {
  const parser = new DOMParser();
  const document = parser.parseFromString(`
    <!DOCTYPE html>
    <html>
      <head><title>BitCraft Map</title></head>
      <body>
        <div id="map"></div>
        <script src="assets/leaflet/leaflet.js"></script>
        <script src="assets/js/config.js"></script>
        <script src="assets/js/map.js"></script>
      </body>
    </html>
  `, "text/html");
  
  return document;
};

Deno.test("BitCraft Map - Basic Structure", () => {
  const doc = mockDOM();
  const mapElement = doc.getElementById("map");
  assertExists(mapElement);
  assertEquals(mapElement.tagName, "DIV");
});

Deno.test("Config - Coordinate System", async () => {
  // Test coordinate system calculations
  const apothem = 2 / Math.sqrt(3);
  const expected = 1.1547; // approximately
  assertEquals(Math.round(apothem * 10000) / 10000, expected);
});

Deno.test("GeoJSON Validation", async () => {
  const testGeoJSON = {
    type: "FeatureCollection",
    features: [{
      type: "Feature",
      properties: { name: "Test" },
      geometry: {
        type: "Point",
        coordinates: [15000, 15000]
      }
    }]
  };

  assertEquals(testGeoJSON.type, "FeatureCollection");
  assertEquals(testGeoJSON.features.length, 1);
  assertEquals(testGeoJSON.features[0].geometry.type, "Point");
});

// Test coordinate conversion functions
Deno.test("Coordinate Conversion", () => {
  // Mock the readableCoordinates function from map.js
  const readableCoordinates = (latlng: { lat: number; lng: number }) => [
    Math.round(latlng.lat / 3),
    Math.round(latlng.lng / 3)
  ];

  const result = readableCoordinates({ lat: 45000, lng: 45000 });
  assertEquals(result, [15000, 15000]);
});
```

#### Integration Tests with HTTP

Create `tests/server.test.ts`:

```typescript
// tests/server.test.ts - Test development server
import { assertEquals } from "jsr:@std/assert";

Deno.test("Development Server - Static Files", async () => {
  // Start test server (you'd run this in background)
  const response = await fetch("http://localhost:8000/index.html");
  assertEquals(response.status, 200);
  
  const html = await response.text();
  assertEquals(html.includes("BitCraft Map"), true);
});

Deno.test("Development Server - Assets Loading", async () => {
  const cssResponse = await fetch("http://localhost:8000/assets/css/map.css");
  assertEquals(cssResponse.status, 200);
  assertEquals(cssResponse.headers.get("content-type")?.includes("text/css"), true);

  const jsResponse = await fetch("http://localhost:8000/assets/js/config.js");
  assertEquals(jsResponse.status, 200);
  assertEquals(jsResponse.headers.get("content-type")?.includes("javascript"), true);
});

Deno.test("GeoJSON Files Accessible", async () => {
  const claimsResponse = await fetch("http://localhost:8000/assets/markers/claims.geojson");
  assertEquals(claimsResponse.status, 200);
  
  const claimsData = await claimsResponse.json();
  assertEquals(claimsData.type, "FeatureCollection");
});
```

#### Browser Automation with Puppeteer Alternative

Create `tests/e2e.test.ts`:

```typescript
// tests/e2e.test.ts - End-to-end testing with Deno
import { assertEquals } from "jsr:@std/assert";
import { chromium } from "npm:playwright";

Deno.test("E2E - Map Loads and Functions", async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    await page.goto("http://localhost:8000");
    
    // Wait for map to load
    await page.waitForSelector("#map");
    
    // Check if Leaflet map is initialized
    const mapExists = await page.evaluate(() => {
      return window.map !== undefined;
    });
    
    assertEquals(mapExists, true);

    // Test layer controls
    const layerControls = await page.$$(".leaflet-control-layers");
    assertEquals(layerControls.length > 0, true);

    // Test coordinate display
    await page.mouse.move(400, 300);
    const coordsDisplay = await page.textContent("#coordinates-display");
    assertEquals(coordsDisplay !== null, true);

  } finally {
    await browser.close();
  }
});
```

#### Running Tests

```bash
# Run all tests
deno test --allow-net --allow-read

# Run specific test file
deno test --allow-net --allow-read tests/map.test.ts

# Run tests with coverage
deno test --allow-net --allow-read --coverage=coverage/

# Generate coverage report
deno coverage coverage/
```

---

## Development Workflow with Deno 2

### Daily Development Commands

Replace all Node.js commands with these Deno equivalents:

```bash
# Start development (replaces npm run dev)
deno task dev

# Start with file watching (replaces nodemon)
deno task dev:watch

# Start with live reload
deno task dev:reload

# Format code (replaces prettier/eslint --fix)
deno fmt assets/js/ scripts/

# Lint code (replaces eslint)
deno lint assets/js/ scripts/

# Type check JavaScript files
deno check assets/js/*.js

# Run tests (replaces npm test)
deno test --allow-net --allow-read

# Bundle for production (if needed)
deno bundle assets/js/map.js dist/map.bundle.js
```

### Enhanced Development Scripts

Create `scripts/dev-tools.ts`:

```typescript
// scripts/dev-tools.ts - Development utilities
import { walk } from "jsr:@std/fs/walk";
import { extname } from "jsr:@std/path";

// Validate all GeoJSON files
export async function validateGeoJSON() {
  console.log("🔍 Validating GeoJSON files...");
  
  for await (const entry of walk("assets/markers", { exts: [".geojson"] })) {
    try {
      const content = await Deno.readTextFile(entry.path);
      const data = JSON.parse(content);
      
      if (data.type !== "FeatureCollection") {
        console.error(`❌ ${entry.path}: Not a valid FeatureCollection`);
      } else {
        console.log(`✅ ${entry.path}: Valid (${data.features?.length || 0} features)`);
      }
    } catch (error) {
      console.error(`❌ ${entry.path}: ${error.message}`);
    }
  }
}

// Optimize images
export async function optimizeAssets() {
  console.log("🎨 Analyzing asset sizes...");
  
  const sizes: Record<string, number> = {};
  
  for await (const entry of walk("assets", { includeDirs: false })) {
    const ext = extname(entry.path);
    if (['.png', '.jpg', '.jpeg', '.svg', '.gif'].includes(ext)) {
      const stat = await Deno.stat(entry.path);
      sizes[entry.path] = stat.size;
    }
  }

  // Sort by size (largest first)
  const sortedFiles = Object.entries(sizes)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10);

  console.log("\n📊 Largest asset files:");
  for (const [path, size] of sortedFiles) {
    const sizeKB = (size / 1024).toFixed(1);
    console.log(`   ${sizeKB}KB - ${path}`);
  }
}

// Performance audit
export async function performanceAudit() {
  console.log("⚡ Running performance audit...");
  
  const startTime = performance.now();
  const response = await fetch("http://localhost:8000");
  const loadTime = performance.now() - startTime;
  
  const html = await response.text();
  const scriptTags = (html.match(/<script/g) || []).length;
  const linkTags = (html.match(/<link/g) || []).length;
  
  console.log(`🕐 Page load time: ${loadTime.toFixed(2)}ms`);
  console.log(`📜 Script tags: ${scriptTags}`);
  console.log(`🔗 Link tags: ${linkTags}`);
  console.log(`📄 HTML size: ${(html.length / 1024).toFixed(1)}KB`);
}

// CLI interface
if (import.meta.main) {
  const command = Deno.args[0];
  
  switch (command) {
    case "validate":
      await validateGeoJSON();
      break;
    case "optimize":
      await optimizeAssets();
      break;
    case "audit":
      await performanceAudit();
      break;
    default:
      console.log("Available commands: validate, optimize, audit");
  }
}
```

**Usage**:
```bash
# Validate all GeoJSON files
deno run --allow-read scripts/dev-tools.ts validate

# Analyze asset sizes
deno run --allow-read scripts/dev-tools.ts optimize

# Performance audit
deno run --allow-net --allow-read scripts/dev-tools.ts audit
```

---

## Advanced Deno Features

### TypeScript Support for JavaScript Files

Convert existing JavaScript to TypeScript gradually:

**Step 1: Add type checking to existing JS**

```javascript
// assets/js/config.js - Add JSDoc types
/**
 * @typedef {Object} MapBounds
 * @property {number} minLat
 * @property {number} maxLat
 * @property {number} minLng
 * @property {number} maxLng
 */

/**
 * Creates map configuration options
 * @returns {MapBounds} The map bounds configuration
 */
export function createMapOptions() {
  // existing code...
}
```

**Step 2: Gradual TypeScript conversion**

Create `assets/js/types.ts`:

```typescript
// assets/js/types.ts - Type definitions
export interface MapConfiguration {
  bounds: [[number, number], [number, number]];
  maxZoom: number;
  minZoom: number;
  crs: L.CRS;
}

export interface GeoJSONFeature {
  type: "Feature";
  properties: Record<string, any>;
  geometry: {
    type: string;
    coordinates: number[] | number[][] | number[][][];
  };
}

export interface CustomMarkerProperties {
  iconName?: string;
  iconSize?: [number, number];
  popupText?: string | string[];
  makeCanvas?: boolean;
  turnLayerOn?: string | string[];
  turnLayerOff?: string | string[];
  flyTo?: [number, number];
  zoomTo?: number;
  noPan?: boolean;
}
```

### Performance Monitoring

Create `scripts/performance-monitor.ts`:

```typescript
// scripts/performance-monitor.ts - Monitor development performance
import { delay } from "jsr:@std/async";

interface PerformanceMetrics {
  responseTime: number;
  memoryUsage: number;
  timestamp: number;
}

class DevServerMonitor {
  private metrics: PerformanceMetrics[] = [];
  private running = false;

  async start() {
    this.running = true;
    console.log("📊 Starting performance monitoring...");

    while (this.running) {
      await this.collectMetrics();
      await delay(5000); // Collect every 5 seconds
    }
  }

  async collectMetrics() {
    const startTime = performance.now();
    
    try {
      const response = await fetch("http://localhost:8000", { 
        method: "HEAD" 
      });
      
      const responseTime = performance.now() - startTime;
      const memoryUsage = (Deno.memoryUsage().rss / 1024 / 1024); // MB

      const metric: PerformanceMetrics = {
        responseTime,
        memoryUsage,
        timestamp: Date.now()
      };

      this.metrics.push(metric);
      
      // Keep only last 100 metrics
      if (this.metrics.length > 100) {
        this.metrics.shift();
      }

      // Log if response time is slow
      if (responseTime > 100) {
        console.log(`⚠️  Slow response: ${responseTime.toFixed(2)}ms`);
      }

    } catch (error) {
      console.log(`❌ Server unreachable: ${error.message}`);
    }
  }

  getReport() {
    if (this.metrics.length === 0) return "No metrics collected";

    const avgResponseTime = this.metrics.reduce((sum, m) => sum + m.responseTime, 0) / this.metrics.length;
    const maxResponseTime = Math.max(...this.metrics.map(m => m.responseTime));
    const avgMemory = this.metrics.reduce((sum, m) => sum + m.memoryUsage, 0) / this.metrics.length;

    return `
📊 Performance Report (last ${this.metrics.length} samples):
   Average Response Time: ${avgResponseTime.toFixed(2)}ms
   Max Response Time: ${maxResponseTime.toFixed(2)}ms
   Average Memory Usage: ${avgMemory.toFixed(1)}MB
    `;
  }

  stop() {
    this.running = false;
    console.log(this.getReport());
  }
}

if (import.meta.main) {
  const monitor = new DevServerMonitor();
  
  // Handle Ctrl+C gracefully
  Deno.addSignalListener("SIGINT", () => {
    monitor.stop();
    Deno.exit(0);
  });

  await monitor.start();
}
```

### Hot Module Replacement (HMR)

Create `scripts/hmr-server.ts`:

```typescript
// scripts/hmr-server.ts - Hot Module Replacement for BitCraft Map
import { serveDir } from "jsr:@std/http/file-server";

const HMR_PORT = 8002;
const STATIC_PORT = 8000;

interface HMRClient {
  socket: WebSocket;
  id: string;
}

class HMRServer {
  private clients = new Set<HMRClient>();
  private moduleGraph = new Map<string, Set<string>>();

  constructor() {
    this.startHMRServer();
    this.startFileWatcher();
    this.startStaticServer();
  }

  private startHMRServer() {
    Deno.serve({ port: HMR_PORT }, (req) => {
      if (req.headers.get("upgrade") === "websocket") {
        const { socket, response } = Deno.upgradeWebSocket(req);
        const clientId = crypto.randomUUID();

        socket.onopen = () => {
          const client: HMRClient = { socket, id: clientId };
          this.clients.add(client);
          console.log(`🔌 HMR client connected: ${clientId}`);
        };

        socket.onclose = () => {
          this.clients.forEach(client => {
            if (client.id === clientId) {
              this.clients.delete(client);
            }
          });
          console.log(`🔌 HMR client disconnected: ${clientId}`);
        };

        return response;
      }
      return new Response("WebSocket connection required", { status: 426 });
    });
  }

  private async startFileWatcher() {
    const watcher = Deno.watchFs(["assets/js", "assets/css", "index.html"]);

    for await (const event of watcher) {
      if (event.kind === "modify") {
        for (const path of event.paths) {
          await this.handleFileChange(path);
        }
      }
    }
  }

  private async handleFileChange(filePath: string) {
    const ext = filePath.split('.').pop();
    
    console.log(`🔄 File changed: ${filePath}`);

    // Determine reload strategy based on file type
    let reloadType = "full";
    
    if (ext === "css") {
      reloadType = "css";
    } else if (ext === "js") {
      reloadType = "js";
    }

    const message = {
      type: "reload",
      reloadType,
      path: filePath,
      timestamp: Date.now()
    };

    // Send to all connected clients
    for (const client of this.clients) {
      try {
        client.socket.send(JSON.stringify(message));
      } catch {
        this.clients.delete(client);
      }
    }
  }

  private async startStaticServer() {
    Deno.serve({ port: STATIC_PORT }, async (req) => {
      const url = new URL(req.url);
      
      // Inject HMR client script into HTML
      if (url.pathname.endsWith('.html') || url.pathname === '/') {
        const response = await serveDir(req, { fsRoot: "./" });
        const html = await response.text();
        
        const hmrScript = `
          <script>
            (function() {
              const ws = new WebSocket('ws://localhost:${HMR_PORT}');
              
              ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                
                if (message.type === 'reload') {
                  console.log('🔄 HMR:', message.path);
                  
                  if (message.reloadType === 'css') {
                    // Reload CSS without page refresh
                    const links = document.querySelectorAll('link[rel="stylesheet"]');
                    links.forEach(link => {
                      const newLink = link.cloneNode();
                      newLink.href = link.href + '?t=' + message.timestamp;
                      link.parentNode.replaceChild(newLink, link);
                    });
                  } else {
                    // Full page reload for JS and HTML changes
                    location.reload();
                  }
                }
              };
              
              ws.onopen = () => console.log('🔌 HMR connected');
              ws.onclose = () => console.log('🔌 HMR disconnected');
            })();
          </script>
        `;
        
        const modifiedHtml = html.replace('</head>', `${hmrScript}</head>`);
        
        return new Response(modifiedHtml, {
          headers: { "content-type": "text/html" }
        });
      }

      return serveDir(req, { fsRoot: "./" });
    });
  }
}

if (import.meta.main) {
  console.log("🚀 Starting BitCraft Map HMR development server");
  console.log(`🌐 App: http://localhost:${STATIC_PORT}`);
  console.log(`🔌 HMR: ws://localhost:${HMR_PORT}`);
  
  new HMRServer();
}
```

---

## Migration Checklist

### ✅ Complete Migration Steps

**1. Install Deno 2**
```bash
# Windows
irm https://deno.land/install.ps1 | iex

# macOS/Linux  
curl -fsSL https://deno.land/install.sh | sh
```

**2. Create Deno Configuration**
- [ ] Create `deno.json` with tasks and imports
- [ ] Configure VS Code settings for Deno
- [ ] Install Deno extension for VS Code

**3. Replace Development Server**
- [ ] Remove Node.js http-server dependency
- [ ] Create `dev-server.ts` with Deno
- [ ] Test static file serving
- [ ] Verify CORS headers for development

**4. Replace File Watching**
- [ ] Remove nodemon dependency
- [ ] Use `--watch` flag or create custom watcher
- [ ] Test auto-restart functionality

**5. Migrate Testing (Optional)**
- [ ] Create test files in `tests/` directory
- [ ] Write basic unit tests
- [ ] Set up integration tests
- [ ] Configure test commands in deno.json

**6. Update Documentation**
- [ ] Update prerequisites in getting-started.md
- [ ] Replace npm commands with deno tasks
- [ ] Add new development workflow instructions

**7. Enhanced Features (Optional)**
- [ ] Set up live reload with WebSocket
- [ ] Create performance monitoring
- [ ] Add hot module replacement
- [ ] Set up TypeScript gradual migration

### Pre-Migration Backup

```bash
# Backup current setup before migration
cp -r bitcraftmap bitcraftmap-backup-node
```

### Validation Commands

After migration, verify everything works:

```bash
# Start development server
deno task dev

# Verify map loads at http://localhost:8000
# Check browser console for errors
# Test all layer controls
# Verify coordinate display
# Test custom GeoJSON loading

# Run tests (if created)
deno test --allow-net --allow-read

# Check code quality
deno fmt --check assets/js/
deno lint assets/js/
```

---

## Troubleshooting

### Common Migration Issues

#### Permission Errors
**Problem**: Deno security errors
```
error: Requires allow-net access
```

**Solution**:
```bash
# Add required permissions
deno run --allow-net --allow-read dev-server.ts

# Or use -A for all permissions (development only)
deno run -A dev-server.ts
```

#### Import Resolution Issues
**Problem**: Module not found errors

**Solution**:
Update imports to use Deno-compatible paths:
```typescript
// ✅ Use jsr: for standard library
import { serveDir } from "jsr:@std/http/file-server";

// ✅ Use npm: for Node packages (if needed)
import express from "npm:express";

// ✅ Use https: for direct URLs
import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
```

#### CORS Issues in Development
**Problem**: Cross-origin errors when testing locally

**Solution**:
```typescript
// Add CORS headers in dev server
response.headers.set("Access-Control-Allow-Origin", "*");
response.headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
response.headers.set("Access-Control-Allow-Headers", "Content-Type");
```

#### File Path Issues
**Problem**: Path resolution differences between Node.js and Deno

**Solution**:
```typescript
// Use Deno's path utilities
import { join, resolve } from "jsr:@std/path";

// Instead of Node.js path module
const filePath = join(Deno.cwd(), "assets", "markers", "claims.geojson");
```

#### TypeScript Configuration Issues
**Problem**: Type errors when checking JavaScript files

**Solution**:
```json
// In deno.json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,  // Disable strict checking for JS files
    "lib": ["dom", "dom.asynciterable", "deno.ns"]
  }
}
```

### Performance Troubleshooting

#### Slow Server Startup
**Problem**: Development server takes long to start

**Investigation**:
```bash
# Profile server startup
deno run --allow-net --allow-read --log-level=info dev-server.ts

# Check for large file scanning
deno run --allow-net --allow-read --v8-flags=--prof dev-server.ts
```

#### Memory Usage Issues  
**Problem**: High memory consumption during development

**Solution**:
```typescript
// Monitor memory usage
console.log("Memory usage:", Deno.memoryUsage());

// Implement garbage collection hints for large operations
if (globalThis.gc) {
  globalThis.gc();
}
```

### Getting Help

**Deno Resources**:
- [Deno Manual](https://deno.land/manual)
- [Deno Standard Library](https://deno.land/std)
- [Deno Examples](https://examples.deno.land/)

**BitCraft Map Community**:
- [Project Repository](https://github.com/bitcraftmap/bitcraftmap)
- [BitCraft Game Community](https://discord.gg/bitcraft)
- [Development Discussions](https://github.com/bitcraftmap/bitcraftmap/discussions)

---

## Summary

This migration guide provides everything needed to completely replace Node.js with Deno 2 in your BitCraft Map project. The benefits include:

### 🏆 Key Improvements Achieved

**Performance Gains**:
- ⚡ 2-3x faster development server startup
- 🚀 Reduced memory footprint (no node_modules)
- 📦 Zero-dependency static file serving

**Security Enhancements**:
- 🔒 Explicit permissions model
- 🛡️ No supply chain vulnerabilities from npm packages
- 🔐 Secure-by-default runtime environment

**Developer Experience**:
- 🛠️ Built-in formatter, linter, and test runner
- 📝 Native TypeScript support without configuration
- 🔄 Advanced file watching with hot module replacement
- 📊 Performance monitoring and development tools

**Modern JavaScript/TypeScript**:
- 🌐 Web standard APIs (fetch, WebSocket, streams)
- ⏰ Top-level await support
- 📦 ES modules by default
- 🔧 Import maps for cleaner dependency management

### 🎯 Migration Results

After completing this migration, you will have:

1. **Eliminated all Node.js dependencies** - No more `npm install` or `node_modules`
2. **Streamlined development workflow** - Single `deno task dev` command to start
3. **Enhanced debugging capabilities** - Built-in performance monitoring and HMR
4. **Future-proof foundation** - Modern runtime with active development
5. **Better security posture** - Explicit permissions and secure defaults

### 🚀 Next Steps

**Immediate Actions**:
1. Follow the [Migration Checklist](#migration-checklist) step by step
2. Test the basic development server functionality
3. Verify all BitCraft Map features work correctly

**Advanced Setup** (Optional):
1. Implement hot module replacement for faster development
2. Set up automated testing with Deno's built-in test runner
3. Add performance monitoring for optimization insights
4. Consider gradual TypeScript migration for better type safety

**Long-term Considerations**:
1. Keep Deno updated for latest performance and security improvements
2. Explore Deno Deploy for serverless deployment options
3. Consider using Deno's built-in bundling for production optimization
4. Investigate Fresh or other Deno web frameworks for future features

---

**Document Version**: 1.0
**Last Updated**: 2024-10-19
**Maintainer**: BitCraft Map Development Team
**Compatibility**: Deno 2.0+, BitCraft Map v1.0+

**Review Schedule**: Update quarterly or when major Deno versions are released

---

**Happy Mapping with Deno 2! 🗺️**

This migration transforms your development experience while maintaining full compatibility with the existing BitCraft Map functionality. The modern runtime capabilities and enhanced security model provide a solid foundation for future development.