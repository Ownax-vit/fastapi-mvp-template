from typing import cast

from fastapi import APIRouter

from src.ai.agents import gender_agent
from src.models.types import Gender

router = APIRouter(prefix="/ai")


@router.get(
    path="",
)
async def receive_gender(name: str) -> Gender:
    res = await gender_agent.run(f"Give me gender: {name}")
    return cast(Gender, res.output)
