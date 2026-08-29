from typing import Literal, Union
from pydantic import BaseModel, Field

class Question(BaseModel):
    question: str = Field(
        description="The generated educational question based strictly on the provided context."
    )

    question_type: Literal["T/F", "MCQ"] = Field(
        description="Must exactly match the requested question type."
    )

    options: list[str] | None = Field(
        description=(
            "For MCQ, provide exactly 4 options as a list of strings. "
            "For T/F, this must be null."
        )
    )

    answer: str = Field(
        description=(
            "For T/F, must be exactly 'True' or 'False'. "
            "For MCQ, must be exactly one option identifier such as 'A', 'B', 'C', or 'D'."
        )
    )

    explanation: str = Field(
        description="A concise explanation supporting the answer using the provided context."
    )

    def format(self) -> str:
        """
        Returns a structured string for display or logging.
        """
        return f"Question: {self.question}\nOptions: {self.options}\nAnswer: {self.answer}\nExplanation: {self.explanation}\n"

class Feedback(BaseModel):
    feedback: str = Field(
        description="feedback about the generated or refined question, such as accuracy, clarity, or educational value."
    )

    def format(self) -> str:
        """
        Formats the feedback message.
        """
        return f"Feedback: {self.feedback}\n"

class GradeQuestion(BaseModel):
    """Represents the grading information for a question."""

    score: str = Field(
        description="The score assigned to the question based on its relevance and quality. Must be 'Yes' or 'No'."
    )
