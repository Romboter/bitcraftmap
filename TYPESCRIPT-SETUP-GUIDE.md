# TypeScript Migration Setup Guide

*Complete configuration files and setup instructions for the BitCraft Map TypeScript migration*

---

## 📋 Quick Start Checklist

When ready to implement the TypeScript migration, create these files in the following order:

1. **Initialize Project Structure**
   - [ ] Create `package.json`
   - [ ] Create `tsconfig.json`
   - [ ] Create `vite.config.ts`
   - [ ] Create `.eslintrc.json`
   - [ ] Create `.prettierrc`
   - [ ] Create `src/` directory structure

2. **Install Dependencies**
   - [ ] Run `npm install` for dependencies
   - [ ] Run `npm run dev` to test setup

3. **Begin Migration**
   - [ ] Start with Phase 1 as outlined in the migration plan

---

## 📦 Configuration Files

### `package.json`
```json
{
  "name": "bitcraft-map",
  "version": "2.0.0",
  "type": "module",
  "description": "Interactive map for BitCraft Online game",
  "main": "dist/index.html",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src --ext ts,tsx --fix",
    "lint:check": "eslint src --ext ts,tsx",
    "format": "prettier --write src/**/*.{ts,tsx,json,md}",
    "format:check": "prettier --check src/**/*.{ts,tsx,json,md}",
    "type-check": "tsc --noEmit",
    "validate": "npm run type-check && npm run lint:check && npm run format:check && npm run test",
    "clean": "rm -rf dist node_modules/.vite",
    "analyze": "npm run build && npx vite-bundle-analyzer dist"
  },
  "keywords": [
    "bitcraft",
    "map",
    "game",
    "leaflet",
    "typescript",
    "interactive"
  ],
  "author": "BitCraft Map Team",
  "license": "MIT",
  "dependencies": {
    "leaflet": "^1.9.4"
  },
  "devDependencies": {
    "@types/leaflet": "^1.9.8",
    "@types/node": "^20.10.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "@typescript-eslint/parser": "^6.13.0",
    "@vitest/coverage-v8": "^1.0.0",
    "@vitest/ui": "^1.0.0",
    "eslint": "^8.54.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-import": "^2.29.0",
    "happy-dom": "^12.10.0",
    "prettier": "^3.1.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vite-bundle-analyzer": "^0.7.0",
    "vitest": "^1.0.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    
    /* Type Checking */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,
    
    /* Module Resolution */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/types/*": ["./src/types/*"],
      "@/config/*": ["./src/config/*"],
      "@/core/*": ["./src/core/*"],
      "@/layers/*": ["./src/layers/*"],
      "@/services/*": ["./src/services/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/ui/*": ["./src/ui/*"]
    }
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "vite.config.ts"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "assets/js/**/*",
    "**/*.test.ts"
  ]
}
```

### `vite.config.ts`
```typescript
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    target: 'es2020',
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
      output: {
        manualChunks: {
          leaflet: ['leaflet'],
          vendor: ['leaflet']
        }
      }
    },
    sourcemap: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  server: {
    port: 3000,
    open: true,
    cors: true
  },
  preview: {
    port: 4173,
    cors: true
  },
  test: {
    environment: 'happy-dom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json-summary'],
      threshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  }
})
```

### `.eslintrc.json`
```json
{
  "root": true,
  "env": {
    "browser": true,
    "es2020": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": ["./tsconfig.json"]
  },
  "plugins": [
    "@typescript-eslint",
    "import"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": [
      "error",
      { "argsIgnorePattern": "^_" }
    ],
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-non-null-assertion": "error",
    "@typescript-eslint/prefer-nullish-coalescing": "error",
    "@typescript-eslint/prefer-optional-chain": "error",
    "import/order": [
      "error",
      {
        "groups": [
          "builtin",
          "external",
          "internal",
          "parent",
          "sibling",
          "index"
        ],
        "newlines-between": "always",
        "alphabetize": {
          "order": "asc",
          "caseInsensitive": true
        }
      }
    ],
    "no-console": "warn",
    "prefer-const": "error",
    "no-var": "error"
  },
  "ignorePatterns": [
    "dist",
    "assets/js",
    "*.config.js",
    "node_modules"
  ]
}
```

### `.prettierrc`
```json
{
  "semi": false,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

### `.gitignore` (updated)
```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/settings.json
.vscode/launch.json
.vscode/tasks.json
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Test coverage
coverage/

# Temporary files
*.tmp
*.temp

# Cache directories
.cache/
.vite/

# Logs
logs/
*.log

# Keep existing files
!assets/
!scripts/
!backend/
!docs/
```

---

## 📁 Directory Structure Setup

Create the following directory structure:

```
src/
├── types/
│   ├── index.ts
│   ├── leaflet.d.ts
│   ├── geojson.d.ts
│   ├── config.d.ts
│   └── map.d.ts
├── config/
│   ├── index.ts
│   ├── mapOptions.ts
│   ├── appOptions.ts
│   └── constants.ts
├── core/
│   ├── index.ts
│   ├── Map.ts
│   ├── LayerRegistry.ts
│   └── EventHandler.ts
├── layers/
│   ├── index.ts
│   ├── BaseLayer.ts
│   ├── ClaimsLayer.ts
│   ├── CavesLayer.ts
│   └── WaypointsLayer.ts
├── services/
│   ├── index.ts
│   ├── GeoJsonService.ts
│   ├── WebSocketService.ts
│   └── ApiService.ts
├── utils/
│   ├── index.ts
│   ├── coordinates.ts
│   ├── validation.ts
│   └── dom.ts
├── ui/
│   ├── index.ts
│   ├── Controls.ts
│   ├── Popups.ts
│   └── Search.ts
├── __tests__/
│   ├── utils/
│   ├── core/
│   └── services/
└── main.ts
```

---

## 🚀 Initial Setup Commands

### 1. Initialize Project
```bash
# Create package.json and install dependencies
npm init -y
# Copy the package.json content above, then:
npm install
```

### 2. Create TypeScript Configuration
```bash
# Create tsconfig.json (copy content above)
# Create vite.config.ts (copy content above)
```

### 3. Set Up Code Quality Tools
```bash
# Create .eslintrc.json and .prettierrc (copy content above)
# Test the setup
npm run type-check
npm run lint
npm run format
```

### 4. Create Directory Structure
```bash
# Create all src directories
mkdir -p src/{types,config,core,layers,services,utils,ui,__tests__/{utils,core,services}}
```

### 5. Start Development
```bash
npm run dev
```

---

## 📋 Migration Phase Implementation

### Phase 1: Foundation Files to Create

1. **src/main.ts**
```typescript
import './styles/main.css'
import { BitCraftMap } from '@/core/Map'
import { createAppOptions, createMapOptions } from '@/config'

async function initializeApp(): Promise<void> {
  const appOptions = createAppOptions()
  const mapOptions = createMapOptions()
  
  const mapInstance = new BitCraftMap('map', mapOptions, appOptions)
  await mapInstance.initialize()
}

initializeApp().catch(console.error)
```

2. **src/types/index.ts**
```typescript
export * from './config.d'
export * from './geojson.d'
export * from './leaflet.d'
export * from './map.d'
```

3. **src/config/index.ts**
```typescript
export { createAppOptions } from './appOptions'
export { createMapOptions } from './mapOptions'  
export * from './constants'
```

---

## 🧪 Testing Setup

### Vitest Configuration
The Vite config includes Vitest settings. Create test files alongside source files:

```
src/
├── utils/
│   ├── coordinates.ts
│   └── coordinates.test.ts
├── core/
│   ├── Map.ts
│   └── Map.test.ts
```

### Example Test File
```typescript
// src/utils/coordinates.test.ts
import { describe, it, expect } from 'vitest'
import { readableCoordinates } from './coordinates'

describe('coordinates', () => {
  it('should convert coordinates correctly', () => {
    const result = readableCoordinates({ lat: 3000, lng: 6000 })
    expect(result).toEqual([1000, 2000])
  })
})
```

---

## 📚 Development Workflow

### Daily Development
```bash
# Start development server
npm run dev

# Run tests in watch mode
npm run test

# Type check
npm run type-check

# Validate all (before commit)
npm run validate
```

### Before Committing
```bash
# Full validation
npm run validate

# Build check
npm run build
```

### Production Build
```bash
# Clean build
npm run clean
npm run build

# Preview production build
npm run preview

# Analyze bundle
npm run analyze
```

---

## 🔄 Migration Path

### Converting Existing JavaScript Files

1. **Rename .js to .ts**
2. **Add type annotations**
3. **Fix TypeScript errors**
4. **Add tests**
5. **Update imports**

### Example Migration Process
```typescript
// Before (JavaScript)
function readableCoordinates(latlng) {
    return [Math.round(latlng.lat / 3), Math.round(latlng.lng / 3)]
}

// After (TypeScript)
import type { LatLng } from '@/types'

export function readableCoordinates(latlng: LatLng): [number, number] {
    return [Math.round(latlng.lat / 3), Math.round(latlng.lng / 3)]
}
```

---

## ⚡ Performance Optimization

### Vite Optimizations
- **Code Splitting**: Automatic with dynamic imports
- **Tree Shaking**: Enabled by default
- **Asset Optimization**: Images, CSS minification
- **Bundle Analysis**: Use `npm run analyze`

### TypeScript Optimizations
- **Strict Mode**: Catch errors early
- **Path Mapping**: Clean imports
- **Type-only Imports**: Better tree shaking

---

## 🎯 Next Steps

1. **Review this setup guide**
2. **Switch to Code mode**
3. **Create the configuration files**
4. **Set up the directory structure**
5. **Begin Phase 1 migration**

---

*This setup guide provides all the configuration needed to begin the TypeScript migration. Once these files are created, follow the migration roadmap in the main plan document.*