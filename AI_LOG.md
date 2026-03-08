(BTS) Airline On-Time Data‎
+20
Lines changed: 20 additions & 0 deletions
Original file line number	Diff line number	Diff line change
AI_LOG.md
# AI Collaboration Log – Foundation 1
## What I Asked
- Asked for guidance on structuring a dataset discovery and architecture exploration deliverable
- Asked for help identifying architectural characteristics relevant to large, relational government datasets
- Asked for clarification on how instructors evaluate “problem space” versus “problem definition”
## What I Got
- Suggested dataset analysis structure
- Examples of candidate architecture characteristics and trade-offs
- Guidance on framing exploratory observations without committing to a final solution
## What I Used, Modified, or Rejected
- Used the architectural characteristic categories but customized explanations to the aviation domain
- Modified candidate problem statements to ensure they were concrete and business-focused
- Rejected suggestions that assumed real-time system requirements, as those are not yet established
## Judgment Calls
I prioritized scalability, data consistency, and evolvability because of the dataset’s size and historical depth. I intentionally avoided committing to availability or low-latency guarantees since the problem definition has not yet been finalized.

---

# AI Collaboration Log – Foundation 3

## Process Description
During Foundation 3, I used AI primarily as a development assistant while building the MVP pipeline. AI helped generate initial code structure, debug errors, and draft documentation. I independently verified all outputs by running the pipeline scripts and checking results in the terminal.

My workflow typically followed this pattern:
1. Implement or attempt code manually.
2. Use AI to diagnose errors or suggest improvements.
3. Test the code locally.
4. Adjust the solution to fit the repository structure and assignment requirements.

## Decision Log

### Decision: Modular Pipeline Design
**What I asked AI:**  
How should I structure the pipeline for acquisition, transformation, and execution?

**AI suggestion:**  
Separate the system into three scripts:
- acquire_data.py
- transform_data.py
- run_pipeline.py

**What I did:**  
Accepted the suggestion.

**Why:**  
This structure improves readability and aligns with the assignment requirement for pipeline iterations.

---

### Decision: Use a Local CSV Dataset
**What I asked AI:**  
What dataset should be used to demonstrate the pipeline?

**AI suggestion:**  
Use a small CSV sample of airline on-time performance data.

**What I did:**  
Created a small `flights_sample.csv` dataset.

**Why:**  
This allowed the pipeline to run locally without external dependencies while still demonstrating the workflow.

---

### Decision: Keep the System Monolithic
**What I asked AI:**  
Should the pipeline be implemented as a distributed system?

**AI suggestion:**  
For a small MVP, keep it monolithic.

**What I did:**  
Accepted the suggestion.

**Why:**  
The dataset size and project scope do not justify distributed system complexity.

---

## AI Failures
Some AI-generated suggestions contained incorrect file paths or incomplete code snippets. These issues were resolved by manually reviewing the code, adjusting file paths, and testing each script independently.

## Verification Practices
All AI-generated code was verified by:

- running Python scripts in the terminal
- confirming row counts from datasets
- checking that transformed CSV files were generated
- reviewing outputs printed by the pipeline

## Judgment Patterns
AI was most helpful for generating initial code structures and documentation drafts. However, I frequently needed to simplify AI suggestions and adapt them to the exact structure of my repository and assignment requirements.