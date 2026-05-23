from fastapi import APIRouter, HTTPException

from app.schemas.pipeline import PipelinePayload
from app.services.pipeline_validator import check_is_dag


router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.post("/parse")
async def parse_pipeline(payload: PipelinePayload):
    if len(payload.nodes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Pipeline must contain at least one node",
        )

    node_count = len(payload.nodes)
    edge_count = len(payload.edges)
    is_dag_compliant = check_is_dag(payload.nodes, payload.edges)

    return {
        "success": True,
        "num_nodes": node_count,
        "num_edges": edge_count,
        "is_dag": is_dag_compliant,
    }
