from typing import cast

import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from src.core.config import settings
from src.models.types import Gender

nest_asyncio.apply()

model = OpenRouterModel(
    "x-ai/grok-4.1-fast",
    provider=OpenRouterProvider(api_key=settings.open_router_api_key),
)


gender_agent = Agent(
    model=model,
    deps_type=str,
    output_type=Gender,
    system_prompt=(
        "Check gender by the name provider. If the name is more likely to be male, return male. If the name is more likely"
        "to be female."
    ),
    instrument=True,
)
