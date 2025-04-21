============================================
🛠️  Brainstorm & Tool Selection
============================================

You will receive a **Task Description**. Before generating any code or detailed answer, follow these six steps:

1. **Restate the Task**  
   - Briefly paraphrase the user’s request to confirm understanding.  
     > “The task is to: {{TASK_DESCRIPTION}}”

2. **Brainstorm ≥3 Distinct Approaches**  
   - Outline at least three high‑level solution strategies (e.g., algorithmic patterns, architectural designs, data‑processing pipelines, UI frameworks).

3. **Map Candidate Tools & Frameworks**  
   - For each approach, list relevant technologies (languages, libraries, frameworks, platforms, APIs).  
     - Example: “Approach A → Python 3.11 + pandas; Approach B → PySpark on Databricks; Approach C → Go + Kafka + Redis.”

4. **Compare & Contrast**  
   - For each approach‑tool combo, give a 2–3‑sentence summary plus clear **Pros** and **Cons** bullets.  
     ```
     • Approach A (Python + pandas)
       – Summary: …  
       – Pros: …  
       – Cons: …
     ```

5. **Recommend Top 2 Alternatives**  
   - Based on criteria (performance, scalability, maintainability, ecosystem maturity, team expertise), rank and justify the **two best** choices.

6. **Transition to Detailed Prompt**  
   - Conclude with:  
     > “I recommend **Approach X** and **Approach Y**.  
     > _Now, using the chosen approach (e.g. Approach X), please apply the detailed coding‑prompt template to generate the final instruction:_”

