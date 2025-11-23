from groq import Groq
from typing import List, Dict
import os

class ContentGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"   # fast + free + powerful

    def generate_with_context(self, prompt: str, context: List[str]) -> str:
        context_text = "\n\n".join(context)

        full_prompt = f"""
Use ONLY the following context extracted from notes:

{context_text}

Now perform this task:

{prompt}

Your answer must stay grounded in the context.
"""

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {e}"

    # QUIZ
    def generate_quiz(self, context: List[str], num_questions: int = 5, quiz_type: str = "mcq") -> Dict:
        """
        Generate a quiz with a strict, clean structure.
        Returns: {"content": <formatted string>}
        """

        if quiz_type == "mcq":
            prompt = f"""
You are an exam generator.

Create exactly {num_questions} multiple-choice questions based ONLY on the context above.

STRICT FORMAT RULES (MUST FOLLOW EXACTLY):
- Start directly with "Q1." (no introductory sentence).
- Each question must have 4 options labeled A), B), C), D).
- Put the correct answer on a separate line starting with "Answer:".
- Leave one blank line between questions.
- Do NOT add explanations after the answer.
- Do NOT add any text before Q1 or after the last answer.

Example of the REQUIRED format:

Q1. <question text>
A) <option 1>
B) <option 2>
C) <option 3>
D) <option 4>
Answer: B

Q2. <question text>
A) ...
B) ...
C) ...
D) ...
Answer: D

(continue like this until Q{num_questions})

Now generate the {num_questions} MCQs in exactly that format.
"""
        elif quiz_type == "scenario":
            prompt = f"""
You are an exam generator.

Create exactly {num_questions} scenario-based questions based ONLY on the context above.

STRICT FORMAT:
Q1. <scenario / problem statement>
Answer: <short model answer>

Q2. <scenario / problem statement>
Answer: <short model answer>

(continue until Q{num_questions})

No introductions, no extra commentary, no explanations after answers.
"""
        else:  # "short"
            prompt = f"""
You are an exam generator.

Create exactly {num_questions} conceptual short-answer questions based ONLY on the context above.

STRICT FORMAT:
Q1. <question>
Answer: <2–4 line answer>

Q2. <question>
Answer: <2–4 line answer>

(continue until Q{num_questions})

No introductions, no extra commentary.
"""

        response = self.generate_with_context(prompt, context)
        return {"content": response}


    # LESSON
    def generate_lesson(self, topic, context):
        prompt = f"""
Create a full lesson on '{topic}' including:
- Learning objectives
- Introduction
- Core concepts
- Examples
- Real-world applications
- Summary
- Exercise
"""
        return self.generate_with_context(prompt, context)

    # STUDY PLAN
    def generate_study_plan(self, chapters, days, difficulty):
        chapter_text = "\n".join(f"- {c}" for c in chapters)

        prompt = f"""
    Create a {days}-day study plan.
    Student level: {difficulty}

    Chapters:
    {chapter_text}

    Format each line as:
    Day X | Topics | Activities | Expected Outcomes
    """

        return self.generate_with_context(prompt, [chapter_text])


    # EXPLAIN AT LEVELS
    def explain_at_levels(self, concept, context):
        prompt = f"""
Explain '{concept}' at 3 levels:
BEGINNER:
INTERMEDIATE:
ADVANCED:
"""
        resp = self.generate_with_context(prompt, context)
        parts = resp.split("\n\n")
        return {
            "beginner": parts[0] if len(parts) else resp,
            "intermediate": parts[1] if len(parts) > 1 else "",
            "advanced": parts[2] if len(parts) > 2 else ""
        }

    # STORY
    def generate_story_mode(self, concept, context):
        return self.generate_with_context(
            f"Explain '{concept}' as a creative story.",
            context
        )

    # MIND MAP
    def generate_mindmap(self, context):
        return self.generate_with_context(
            "Generate a hierarchical mindmap of key concepts.",
            context
        )

    # SUMMARY
    def generate_summary(self, context):
        return self.generate_with_context("Summarize all key ideas.", context)

    # FLASHCARDS
    def generate_flashcards(self, context, num_cards=10):
        return self.generate_with_context(
            f"Generate {num_cards} flashcards (front/back).",
            context
        )
