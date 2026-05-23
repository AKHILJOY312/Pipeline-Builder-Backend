from fastapi import APIRouter, HTTPException

from app.constants.messages import API_MESSAGES
from app.constants.routes import ROUTES
from app.constants.status_codes import HTTP_STATUS
from app.schemas.pipeline import PipelinePayload
from app.services.pipeline_validator import check_is_dag


router = APIRouter(prefix=ROUTES.PIPELINES_PREFIX, tags=["pipelines"])


@router.post(ROUTES.PIPELINES_PARSE)
async def parse_pipeline(payload: PipelinePayload):
    if len(payload.nodes) == 0:
        raise HTTPException(
            status_code=HTTP_STATUS.BAD_REQUEST,
            detail=API_MESSAGES.PIPELINE_EMPTY,
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
