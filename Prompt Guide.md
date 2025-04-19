Based on the detailed insights from the provided document, I've integrated state-of-the-art prompt engineering techniques into a refined, advanced, and practical guide specifically for crafting prompts aimed at solving programming tasks. Here's your optimized, comprehensive guide:

---

# 🚀 Advanced Guide for Crafting Programming Prompts (State-of-the-Art Techniques)

This guide leverages cutting-edge prompt engineering practices optimized for GPT-4 and newer reasoning models (such as O1), ensuring your prompts lead to accurate, efficient, secure, and maintainable solutions.

---

## 🔖 Step 1: Define a Clear and Specific Instruction

Explicitly state your task objective in precise terms.

- **Enhanced Example:**  
  > *"Write a Python 3.11 function named `filter_even_sum` that accepts a list of integers and returns the sum of even integers only."*

---

## 📑 Step 2: Provide Comprehensive Context

Include relevant technical details that clearly frame your prompt.

- **Include:**
  - Programming language version
  - Frameworks, libraries, or APIs (use or avoid)
  - Execution environment (local IDE, Databricks, cloud)

- **Advanced Example:**  
  > *"Using PySpark in a Databricks notebook, create a function that aggregates user events stored in a Delta table named 'user_events', grouping by user ID."*

---

## 🧮 Step 3: Structured Task Decomposition (Chain-of-Thought)

Encourage explicit step-by-step reasoning to boost accuracy.

- **Technique:** Structured Chain-of-Thought (SCoT)  
  Prompt explicitly for intermediate reasoning steps, pseudo-code, or structured problem breakdown.

- **Example Prompt:**
  > *"Approach this problem step by step: First, outline a plan or pseudocode. Then, implement the function based on this plan."*

---

## 📌 Step 4: Provide Few-shot Examples (When Applicable)

Use brief examples to clearly illustrate desired output patterns.

- **Example:**  
```python
# Example Input:
[3, 4, 7, 10, 15]

# Example Output:
14  # Explanation: 4 + 10
```

---

## ⚠️ Step 5: Specify Edge Cases and Constraints Clearly

Explicitly guide the model to anticipate and handle potential pitfalls.

- **Common Constraints:**
  - Input size and scalability
  - Handling empty or invalid inputs
  - Performance complexity (Big O notation)
  - Memory management

- **Example:**
  > *"Your function must handle empty lists gracefully by returning `0`. The solution must scale linearly (O(n)) and avoid recursion."*

---

## 🎭 Step 6: Set the Role and Tone (Role Prompting)

Use roles to shape the style and depth of the response.

- **Role Examples:**
  - "Act as a senior Python developer reviewing code."
  - "You are a data scientist mentoring a junior colleague."

- **Advanced Prompt:**
  > *"Act as an experienced software engineer specializing in PySpark. Write code with clear explanatory inline comments."*

---

## 🧹 Step 7: Prompt for Maintainable, Efficient, and Secure Code

Explicitly instruct the model to adhere to best practices.

- **Include explicitly:**
  - Coding style (e.g., PEP 8)
  - Security (e.g., avoiding SQL injections, validating inputs)
  - Efficiency (complexity constraints, memory optimization)

- **Advanced Example:**
  > *"Write the function following PEP 8 style guidelines, include error handling, and optimize for memory and execution efficiency."*

---

## 🛠️ Step 8: Iterative Self-Improvement (Recursive Criticism and Improvement - RCI)

Encourage the model to critique its output and self-optimize.

- **RCI Prompt Example:**
  > *"Generate the code. Afterward, review your code for efficiency, maintainability, and security issues, then provide a revised and improved version."*

---

## 🔍 Step 9: Prompt Evaluation and Testing (Test-Driven Prompting)

Incorporate tests or checks to validate outputs proactively.

- **Testing Example Prompt:**
  > *"Implement the function. Then include three test cases demonstrating typical, boundary, and empty inputs. Confirm your implementation passes all tests."*

- **Explicit Testing Prompt:**
```python
# Tests your function must pass:
assert filter_even_sum([1, 2, 3, 4]) == 6
assert filter_even_sum([]) == 0
assert filter_even_sum([1, 3, 5]) == 0
```

---

## 📚 Step 10: Explicitly Request Documentation and Explanations

Prompt clearly for documentation, docstrings, and inline comments.

- **Example Prompt:**
  > *"Include a Pythonic docstring that briefly explains the purpose, parameters, return values, and an example usage."*

---

## 🔁 Step 11: Evaluate Prompt Effectiveness (Continuous Improvement)

Evaluate the success of your prompts based on:

- Code correctness and unit test pass rates
- Readability, maintainability, and efficiency of the generated code
- Feedback and revisions required (measure iterations)

- **Practical Tip:** Maintain a prompt registry or iterative log, tweaking prompts based on outcomes and edge-case performances.

---

## 🎖️ Complete Advanced Prompting Template for Coding Tasks

Here's a robust, fully-fledged template for solving programming tasks:

> **Task:** "Write a Python function named `calculate_prime_factors` that calculates all prime factors of a given integer."
>  
> **Context:** "Use Python 3.11 with standard libraries only. Intended environment: Local execution."
>  
> **Step-by-step:** "First, clearly outline your algorithm in pseudocode. Then implement the Python function following the outlined approach."
>  
> **Examples:**
> ```python
> # Input:
> 12
> # Output:
> [2, 2, 3]
> ```
>  
> **Constraints:** "Ensure O(sqrt(n)) complexity. Gracefully handle inputs less than 2 by returning an empty list."
>  
> **Role:** "Act as an experienced Python software engineer mentoring a junior developer."
>  
> **Quality:** "Follow PEP 8, include explanatory inline comments and a descriptive docstring."
>  
> **Security & Efficiency:** "Write secure, efficient code and explicitly check for possible edge cases."
>  
> **Iterative Review:** "After initial implementation, critique and revise your code for efficiency, readability, and edge-case handling."
>  
> **Testing:** "Provide three distinct test cases including typical usage, an edge case (e.g., `1`), and a larger number."
>  
> **Documentation:** "Include a brief, clear docstring describing the function, its parameters, return value, and one example."

---

Following this enhanced guide ensures your prompts maximize the potential of advanced language models, leading to high-quality, reliable outputs suitable for professional-grade software development and data science tasks.
