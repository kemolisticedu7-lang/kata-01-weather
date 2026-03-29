# Architecture Reflection

## What Changed

Compared to Foundation 2, my architecture became more concrete and implementation-focused.

Originally, I designed a conceptual pipeline architecture. In Foundation 4, I implemented it as a working system with:

- A runnable Python pipeline (`run_pipeline.py`)
- Explicit functions for loading, transforming, and saving data
- A structured output folder

The biggest change was moving from theory to actual execution and seeing how components interact in practice.

---

## What I Learned

I learned that software architecture is not just about diagrams—it is about making decisions that affect implementation.

Key lessons:
- Data quality is critical; even small issues (like missing files) break the system
- Simpler architectures (modular monolith) are easier to implement and debug
- Clear separation of pipeline stages improves maintainability
- Documentation is as important as code for understanding the system

---

## Trade-offs Revisited

In Foundation 2, I prioritized:

- Evolvability
- Data consistency
- Scalability

In practice:

- **Evolvability worked well** — I could modify the pipeline easily
- **Data consistency required effort** — file paths and inputs caused real issues
- **Scalability was not fully tested** due to using a small dataset

### What surprised me:
- Small operational issues (like file locations) matter a lot in real systems
- Testing is more important than expected for catching errors early

---

## If I Started Over

If I started again, I would:

- Set up a clearer folder structure from the beginning
- Add automated tests earlier (pytest)
- Use configuration files instead of hardcoding file paths
- Start with better data validation from day one

---

## Final Reflection

This project helped me understand how architectural decisions translate into real systems.

I now better understand:
- How pipeline architectures work in practice
- How trade-offs affect system behavior
- How to balance simplicity vs scalability

This experience improved my ability to think like a software architect rather than just a programmer