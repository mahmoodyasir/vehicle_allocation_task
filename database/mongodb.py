import asyncio
import os

import certifi
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from error.exception import ImproperConfigurationError


client: AsyncIOMotorClient | None = None

async def init(test: bool, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> None:
    db_name = os.environ.get('MONGO_DATABASE', None)
    prod = os.environ.get('PRODUCTION', "false")
    if prod == 'false' and not test:
        db_name += '_dev'
    elif prod == 'false' and test:
        db_name += '_test'


    conn_params = {
        'host': os.environ.get('MONGO_HOST', None),
        'username': os.environ.get('MONGO_USERNAME', None),
        'password': os.environ.get('MONGO_PASSWORD', None)
    }
    
    
    if all(conn_params.values()):
        global client
        client = AsyncIOMotorClient(
            host=conn_params['host'],
            username=conn_params['username'],
            password=conn_params['password'],
            uuidRepresentation='standard',
            tlsCAFile=certifi.where(),
            io_loop=loop,
        )

        print(await client.server_info())
    else:
        raise ImproperConfigurationError
                
    if db_name is not None:
        await init_beanie(database=client[db_name], document_models=[
            "employee.model.Employee",
            
        ],
        allow_index_dropping=True,
        recreate_views=True)

        return client, db_name
    else:
        raise ImproperConfigurationError
    

async def close():
    global client
    if client is not None:
        client.close()