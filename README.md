# Malmö Skyttegille Pistolsektion - Rotation Target Backend Resources

This repository contains resources and documentation for Malmö Skyttegille Pistolsektion's custom software for the Eigenbrod TP2 Rotation Target System.

## Overview

This repository provides:

- **OpenAPI Specification** for the REST API and SSE (Server-Sent Events) endpoints
- **Program files** for shooting sequences
- **Audio files** for use with the target system

## Contents

- `openapi/openapi.yaml` — OpenAPI 3.1 specification for the REST API
- `openapi/sse.yaml` — OpenAPI-style documentation for SSE events
- `programs/` — Example and template program files
- `audios/` — Audio files for use with the system

## Related Projects

- **Backend (ESP32 MicroPython):**  
  [rotation_target_backend_esp32_micropython](../rotation_target_backend_esp32_micropython)
- **Frontend (Web App):**  
  [rotation_target_frontend_webapp](../rotation_target_frontend_webapp)

## License

MIT. See [LICENSE](./LICENSE) for details.