from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from quixstreams import Application

import time
import os
import json

kakfa_app = Application(
    broker_address='localhost:9092',
    loglevel='DEBUG',
)

app = FastAPI()

# set up model for sensor data
class SensorEvent(BaseModel):
    sensor_id: str = Field(..., examples=['sensor-123'])
    region: str = Field(..., examples=['us-west'])
    ts: float = Field(..., examples=[180000000.0])
    value: float = Field(..., examples=[12.4, 0.01])
    meta: dict = Field(default_factory=dict)

@app.post('/ingest')
async def get_ingest(evt: SensorEvent):
    payload = evt.model_dump()
    payload['received_ts'] = time.time()
    
    try:
        with kakfa_app.get_producer() as producer:

            producer.produce(
                topic='sensor_events',
                value=json.dumps(payload)
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'ok'}

@app.get('/traces')
async def get_traces():
    pass

@app.get('/test')
def get_test():
    pass
