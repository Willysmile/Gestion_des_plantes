# Security & Vulnerability Management

## Current Status: 2 Moderate npm Vulnerabilities

### Vulnerabilities Detected

**Package:** esbuild <=0.24.2 (transitive via Vite)
- **Severity:** Moderate (GHSA-67mh-4wv8-2f99)
- **Type:** Development-only (dev dependency)
- **Issue:** Allows CSRF-like requests from websites to dev server
- **Affected:** Vite 5.0-6.1.6
- **Production Impact:** None (esbuild only used during dev/build)

### Why We're Not Forcing the Fix

```
Option A: npm audit fix --force
  - Upgrades Vite 5.0 → 7.1.12 (BREAKING CHANGE)
  - Requires code refactoring
  - Not recommended for MVP phase

Option B: Keep Vite 5.0 (CURRENT CHOICE)
  - Only affects dev environment
  - Low practical risk (attacker needs user to visit malicious site)
  - Can upgrade to Vite 7 in Phase 3
  - Zero production impact
```

### Risk Assessment

| Factor | Risk Level | Notes |
|--------|-----------|-------|
| **Exposure** | Low | Dev-only, localhost:5173 |
| **Attack Vector** | Low | Requires user visits malicious site during dev |
| **Production** | None | esbuild not deployed to prod |
| **Timeline** | Phase 3 | Safe to upgrade later |

### Mitigation Strategies (Dev Environment)

✅ **What we're doing:**
- Dev server only accessible from localhost (default)
- HTTPS in dev can be configured if needed
- Code review before production build

🔒 **Additional safeguards (if needed):**
1. Never expose dev server to internet
2. Use `--host 127.0.0.1` only (already default)
3. Disable HMR if paranoid
4. Use firewall rules

### Upgrade Plan (Phase 3)

**When:** After Phase 2 stabilizes
**How:** 
```bash
npm install vite@latest --save-dev
# Test thoroughly
npm run build
# Verify no breaking changes
```

**Vite 5 → 7 Changes:**
- esbuild updated
- Performance improved
- New features available
- Minimal breaking changes

### Documentation

```bash
# Check vulnerabilities anytime
npm audit

# See vulnerable packages
npm audit --json | jq '.vulnerabilities'

# Fix without breaking changes
npm audit fix  # Current (no changes needed)

# Force breaking changes (Phase 3)
npm audit fix --force
```

### Compliance Notes

✅ **For production:**
- Build uses esbuild once (no transitive vulnerability)
- Built assets are static files (no CSRF risk)
- Dev dependencies not shipped

✅ **For development:**
- Team knows about vulns
- Mitigations in place
- Plan to upgrade documented

---

## Dependencies Security Summary

| Package | Version | Type | Security | Notes |
|---------|---------|------|----------|-------|
| react | 18.2.0 | direct | ✅ Safe | Active LTS |
| react-dom | 18.2.0 | direct | ✅ Safe | Active LTS |
| react-router-dom | 6.20.0 | direct | ✅ Safe | Latest stable |
| axios | 1.6.0 | direct | ✅ Safe | Stable |
| tailwindcss | 3.3.6 | dev | ✅ Safe | Latest patch |
| vite | 5.0.0 | dev | ⚠️ Minor | Known: esbuild issue |
| esbuild | <0.24.2 | transitive | ⚠️ Minor | Dev-only impact |

---

Generated: 26 Oct 2025
Last Review: npm audit
