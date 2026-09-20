# DevOps Environment Documentation

## Overview

This document describes the local development environment setup, Docker configuration, PostgreSQL service management, and CI workflow for the P5-B Campus Helpdesk & Maintenance Tickets project.

The goal is to provide a consistent setup process for all team members.

---

# 1. Requirements

Before running the project environment, make sure the following tools are installed:

- Git
- Docker Desktop
- Docker Compose
- WSL 2 (Windows)

Verify installations:

```powershell
docker --version
docker compose version
git --version