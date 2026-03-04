from fastapi import APIRouter

from src.ai.agents import roulette_agent
from src.models.types import Gender

router = APIRouter(prefix="/ai")


@router.get(
    path="",
)
async def receive_users(name: str) -> Gender:
    res = await roulette_agent.run(f"Give me gender: {name}")
    return res.output
