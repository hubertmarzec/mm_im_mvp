from fastapi import APIRouter, HTTPException

from ..models.schemas import RequestList, RequestResponse

router = APIRouter()

    
@router.get("/request/{request_id}", response_model=RequestResponse)
async def get_request(request_id: str):
    if request_id == "invalid-id":
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )
    
    return RequestResponse(
        request_id=request_id,
        status="pending",
        result=None
    )

@router.get("/request", response_model=RequestList)
async def list_requests():
    # Example response with one request
    example_request = RequestResponse(
        request_id="abc",
        status="pending",
        result=None
    )
    
    requests = [example_request]  # Lista z jednym przykładowym requestem
    return RequestList(
        requests=requests,
        total=len(requests)
    )
