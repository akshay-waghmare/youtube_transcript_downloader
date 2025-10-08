# Spec-Driven Development - Quick Reference

## 🚀 **Start Here for Any New Feature**

```bash
# 1. Constitution (Project Principles)
/speckit.constitution

# 2. Specification (What & Why)
/speckit.specify

# 3. Clarification (Reduce Ambiguity) - RECOMMENDED
/speckit.clarify  

# 4. Planning (Tech Stack & How)
/speckit.plan

# 5. Task Breakdown (Actionable Steps)
/speckit.tasks

# 6. Implementation (Execute)
/speckit.implement
```

## 📋 **Optional Quality Commands**

```bash
# Cross-artifact consistency check (after tasks, before implement)
/speckit.analyze

# Generate quality validation checklists
/speckit.checklist
```

## ⚡ **Key Rules**

1. **Always start with `/speckit.constitution`**
2. **Keep "what" separate from "how"** (specify → plan)
3. **Clarify before planning** to avoid rework
4. **Follow the order** - don't skip steps
5. **Constitution guides all technical decisions**

## 🎯 **For This Project Specifically**

- Focus on Python CLI tools for YouTube transcript downloading
- Emphasize error handling, user experience, and performance
- Follow TDD approach with comprehensive test coverage
- Design for cross-platform compatibility
- Support multiple output formats (JSON, text, etc.)

## 📁 **File Locations**

- Constitution: `.specify/memory/constitution.md`
- Specs: `.specify/specs/[number]-[feature-name]/`
- Current branch shows active feature

## 🔍 **Quick Check**

Before implementation, verify:
- [ ] Constitution established
- [ ] Specification complete and clear
- [ ] Technical plan aligns with constitution
- [ ] Tasks are actionable and ordered
- [ ] All dependencies identified

**Remember: Specifications drive implementation, not the reverse!**