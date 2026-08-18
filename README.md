<div align="center">

# 🛡️ AI Agent Permission Firewall

**A zero-trust security & interception layer for autonomous AI agent tool executions.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

</div>

## 📖 Overview

As AI agents gain autonomous access to databases, local file systems, and external APIs, preventing unintended destructive actions becomes critical. 

**AI Agent Permission Firewall** acts as an inline proxy and policy engine. It intercepts tool calls before execution, evaluates action risk levels, blocks unauthorized/hazardous operations, and mandates **Human-in-the-Loop (HITL)** dynamic approval for sensitive operations.

---

## ✨ Key Features

- 🛑 **Tool Execution Interception**: Wraps around dangerous function calls and evaluates them against agent security policies.
- ⚡ **Dynamic Risk Evaluation**: Classifies tool actions (`read_file` vs. `delete_database`) into low and high risk levels.
- 🔐 **Human-in-the-Loop (HITL) Approval Engine**: Halts high-risk requests immediately and issues single-use UUID approval tickets.
- 👨‍💻 **Admin Authorization Override**: Unlocks blocked operations dynamically upon authorized administrator approval.
- 📜 **Centralized Audit Logging**: Captures comprehensive UTC-timestamped decision logs (`ALLOWED`, `BLOCKED`, `PENDING_APPROVAL`) across all invocations.
- 🧪 **Fully Tested**: Built-in `pytest` coverage for endpoint integration and security pipeline checks.

---

## 🏗️ Architecture Flow

```text
[ AI Agent ] ──( 1. Execute Tool )──► [ Permission Firewall ]
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
             [ Low-Risk Action ]                         [ High-Risk Action ]
                       │                                           │
             ( Auto-Approved )                              ( Blocked & Queued )
                       │                                           │
                       ▼                                           ▼
              [ Execute Tool ]                            [ Issue Approval ID ]
                       │                                           │
                       │                                    [ Admin Approves ]
                       │                                           │
                       └───────────────────┬───────────────────────┘
                                           ▼
                                [ Central Audit Log ]