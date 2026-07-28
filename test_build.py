import asyncio
from backend.orchestrator.swarm_manager import SwarmManager

async def test():
    print('Starting build test...')
    manager = SwarmManager()
    try:
        result = await manager.spawn_swarm('Build a basic react app', '')
        print('Build succeeded!')
    except Exception as e:
        print(f'Build failed with error: {e}')
        import traceback
        traceback.print_exc()

asyncio.run(test())
