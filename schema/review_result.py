# schema\review_result.py

from pydantic import BaseModel, Field


class Verdict(BaseModel):
    name: str = Field(description="")
    passed: bool = Field(description="")
    comment: str = Field(description="")


class ReviewerResult(BaseModel):
    criteria: list[Verdict] = Field(description="")
    patterns: list[Verdict] = Field(description="")
    main_problem: str = Field(description="")
    strengths: str = Field(description="")
