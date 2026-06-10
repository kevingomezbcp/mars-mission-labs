# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "agent-framework-openai",
#     "python-dotenv",
# ]
# ///
"""MISION MARTE - Fase 01: conversacion interactiva."""
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
    client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    mission_control = client.as_agent(name="MissionControl", instructions=INSTRUCTIONS)

    # La sesion guarda la memoria de la conversacion
    session = mission_control.create_session()

    print("Control de Mision en linea. Escribe 'salir' para terminar.\n")
    while True:
        user = input("Tú: ")
        if user.strip().lower() in {"salir", "exit", "quit"}:
            print("Cierre de comunicaciones. Cambio y fuera.")
            break

        # session=session  ->  el agente recuerda lo dicho antes
        print("CONTROL: ", end="", flush=True)
        async for chunk in mission_control.run(user, session=session, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
