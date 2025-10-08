# GitHub Copilot Instructions for YouTube Transcript Downloader

## Project Overview
This is a **YouTube Transcript Downloader** project that follows **Spec-Driven Development** methodology using GitHub's Spec Kit. All development must follow the structured workflow outlined below.

## Spec-Driven Development Workflow

We use a **structured, specification-first approach** where requirements and specifications drive implementation, not the other way around. This ensures high-quality, well-planned development.

### 🎯 **Core Philosophy**
- **Specifications are executable** - they directly generate working implementations
- **Intent-driven development** - define the "what" before the "how"
- **Multi-step refinement** rather than one-shot code generation
- **Quality through structure** - each phase builds upon the previous one

### 📋 **Mandatory Development Phases**

#### **Phase 1: Establish Project Principles** 
**Command: `/speckit.constitution`**
- **ALWAYS START HERE** for any new feature or major change
- Define project governance, coding standards, testing requirements
- Establish development guidelines that will govern all subsequent decisions
- Update `.specify/memory/constitution.md` with concrete principles
- These principles must guide all technical decisions

#### **Phase 2: Create Functional Specifications**
**Command: `/speckit.specify`**
- Focus on **WHAT** we're building and **WHY**, not the tech stack
- Create detailed user stories and functional requirements
- Be explicit about requirements - avoid ambiguity
- Do NOT discuss implementation details or technology choices
- Output goes to `.specify/specs/[feature-number]-[feature-name]/spec.md`

#### **Phase 3: Clarify Requirements (Recommended)**
**Command: `/speckit.clarify`**
- **Run this BEFORE planning** to reduce downstream rework
- Ask structured questions to identify ambiguous areas
- Record clarifications in the specification
- Skip only for experimental/spike work (state this explicitly)

#### **Phase 4: Technical Implementation Planning**
**Command: `/speckit.plan`**
- NOW specify your tech stack, architecture, and technical approach
- Reference the constitution principles for guidance
- Create detailed implementation plans with your chosen technologies
- Output includes `plan.md`, `data-model.md`, `research.md`, and contract specifications

#### **Phase 5: Task Breakdown**
**Command: `/speckit.tasks`**
- Generate actionable, ordered task lists from the implementation plan
- Include dependencies and parallel execution opportunities
- Follow TDD approach as defined in constitution
- Output to `.specify/specs/[feature-name]/tasks.md`

#### **Phase 6: Implementation Execution**
**Command: `/speckit.implement`**
- Execute all tasks according to the plan
- Follow the task order and dependencies
- Validate against specifications continuously
- Run tests and quality checks as defined

### 🔍 **Optional Quality Enhancement Commands**

#### **Cross-Artifact Analysis**
**Command: `/speckit.analyze`**
- Run after `/speckit.tasks`, before `/speckit.implement`
- Checks consistency across constitution, spec, plan, and tasks
- Identifies gaps or misalignments

#### **Quality Checklists**
**Command: `/speckit.checklist`**
- Generate custom validation checklists
- Ensure requirements completeness, clarity, and consistency
- Like "unit tests for English specifications"

## 🚫 **What NOT to Do**

1. **Never skip the constitution step** - it's the foundation for all decisions
2. **Don't jump straight to implementation** - always follow the workflow phases
3. **Don't mix "what" and "how"** - keep specification and planning separate
4. **Don't assume requirements** - clarify ambiguity through the structured process
5. **Don't ignore the constitution** - all technical decisions must align with established principles

## 🎯 **Specific Guidelines for This Project**

### For YouTube Transcript Downloader Features:
- **Constitution must address**: Code quality standards, testing approach, user experience consistency, performance requirements, error handling strategy
- **Specifications should cover**: User workflows, supported video formats, transcript formats, storage mechanisms, error scenarios
- **Planning should consider**: Python ecosystem, CLI design, library dependencies, data processing efficiency
- **Implementation must include**: Comprehensive error handling, user-friendly CLI, proper logging, test coverage

### Quality Standards:
- All code must have corresponding tests (TDD approach)
- User-facing features require clear documentation
- Error messages must be helpful and actionable
- Performance considerations for large transcript files
- Security considerations for API usage and data handling

### Technology Preferences:
- Python-first approach for core functionality
- CLI-first interface design
- Library-based architecture for reusability
- JSON and human-readable output formats
- Cross-platform compatibility

## 🔄 **Iterative Development**

For ongoing development:
1. **New features**: Follow the complete workflow from constitution review
2. **Enhancements**: Review constitution alignment, update specs, plan, implement
3. **Bug fixes**: Reference existing specs, update if needed, implement with tests

## 📁 **File Structure Understanding**

```
.specify/
├── memory/
│   └── constitution.md          # Project principles (updated via /speckit.constitution)
├── specs/
│   └── [feature-number]-[name]/ # Feature specifications
│       ├── spec.md              # Functional requirements
│       ├── plan.md              # Technical implementation plan
│       ├── tasks.md             # Actionable task breakdown
│       ├── data-model.md        # Data structures and schemas
│       └── contracts/           # API specs, interfaces
└── templates/                   # Templates for consistency
```

## 🤖 **Agent Behavior**

As an AI agent working on this project:

1. **Always verify workflow compliance** - check which phase we're in
2. **Reference the constitution** - ensure all decisions align with established principles
3. **Maintain specification integrity** - don't implement features not in the spec
4. **Follow the structured process** - don't skip steps or combine phases inappropriately
5. **Ask for clarification** - if specs are unclear, use `/speckit.clarify` or ask directly
6. **Validate continuously** - check implementation against specifications
7. **Update documentation** - keep specs and plans in sync with implementation

## 🎪 **Success Indicators**

You're following the process correctly when:
- ✅ Constitution exists and guides decisions
- ✅ Specifications are clear and complete before planning
- ✅ Technical plans reference the constitution
- ✅ Implementation matches the specifications
- ✅ Tests validate requirements compliance
- ✅ Documentation is current and helpful

Remember: **Specifications drive implementation, not the other way around!**
