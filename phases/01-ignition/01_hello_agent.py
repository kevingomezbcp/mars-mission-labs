# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "agent-framework-openai",
#     "python-dotenv",
# ]
# ///
"""MISION MARTE - Fase 01: tu primer agente."""
import asyncio
import os

from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()

INSTRUCTIONS = (
    "Eres el Control de Mision de MISION MARTE. Coordinas la mision a Marte "
    "y das briefings tecnicos a la tripulacion. Usa terminologia espacial y se conciso. "
    "Responde directamente, sin anteponer tu nombre ni etiquetas como 'MissionControl:'."
)


async def main() -> None:
    # Cliente del modelo (OpenAI)
    client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Crear el agente con su rol
    mission_control = client.as_agent(name="MissionControl", instructions=INSTRUCTIONS)

    # Una consulta, una respuesta completa
    response = await mission_control.run("Control, solicito briefing del estado de la mision.")
    print(f"CONTROL: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
