from pydantic import BaseModel


class NodeSchema(BaseModel):
    id: str
    type: str


class EdgeSchema(BaseModel):
    id: str
    source: str
    target: str


class PipelinePayload(BaseModel):
    nodes: list[NodeSchema]
    edges: list[EdgeSchema]
