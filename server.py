import json
from pathlib import Path

from mcp.server import MCPServer
from pydantic import BaseModel, Field


DATA_FILE = Path(__file__).parent / "postings.json"

with DATA_FILE.open() as f:
    POSTINGS = json.load(f)


mcp = MCPServer("Revelio Workforce MCP")


class SkillSearch(BaseModel):
    skill: str = Field(
        min_length=2,
        max_length=50,
        description="A skill such as Python, Rust, SQL, or OAuth"
    )


class CompanyQuery(BaseModel):
    company: str = Field(
        min_length=2,
        max_length=100,
        description="Company name to count job postings for"
    )


@mcp.tool()
def search_postings_by_skill(query: SkillSearch) -> list[dict]:
    
    skill = query.skill.strip().lower()

    if not skill:
        raise ValueError("Skill cannot be empty.")

    matches = [
        posting
        for posting in POSTINGS
        if skill in [s.lower() for s in posting["skills"]]
    ]

    return [
        {
            "id": posting["id"],
            "company": posting["company"],
            "title": posting["title"],
            "skills": posting["skills"],
        }
        for posting in matches
    ]


@mcp.tool()
def count_postings_by_company(query: CompanyQuery) -> dict:
   
    company = query.company.strip().lower()

    if not company:
        raise ValueError("Company cannot be empty.")

    matches = [
        posting
        for posting in POSTINGS
        if posting["company"].lower() == company
    ]

    return {
        "company": query.company.strip(),
        "count": len(matches),
    }


if __name__ == "__main__":
    mcp.run()