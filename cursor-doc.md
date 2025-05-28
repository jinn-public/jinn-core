# 🌪️ Jinn – Joint Intelligence Non-Profit Network

**Jinn** is a non-profit, open-source platform to simulate financial risk and economic systems.  
We are building **public infrastructure** for civic foresight—tools that allow anyone to model and understand systemic shocks without relying on private black-box systems.

---

## 🧭 Mission

> Build an open simulation engine for financial risk that is modular, transparent, and accessible to the public.

The goal of this MVP is to create a **minimal, working simulation engine** that:
- Accepts structured input (JSON)
- Applies a basic financial model
- Outputs an interpreted result (e.g. change in GDP)
- Can be expanded with more models in the future

---

## ✅ MVP Focus

### Title: **Interest Rate Shock Model**

The MVP models the effect of a change in interest rates on national GDP using a simplified formula.

### Input (JSON):
- `gdp`: total GDP in USD
- `interest_rate_change`: percent increase or decrease

### Output (JSON):
- New GDP estimate
- GDP change
- Assumptions used

---

## 🗂️ Folder Structure

```bash
src/
  engine.py          # Main entry for simulation
  models/
    interest_rate.py # Basic economic model
  utils/             # Reusable math or formatting tools

examples/
  scenario_01.json   # Test scenario input

tests/
  test_engine.py     # Basic unit tests

docs/
  roadmap.md         # Project milestones and goals
