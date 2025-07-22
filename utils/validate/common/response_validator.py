from exception.common.response_exception import ResponseMismatchError

def validate_response_rooms(requested_rooms, response_rooms):
    """요청/응답 방 리스트의 biz_item_id 일치 여부 검증"""
    req_ids = set(r.biz_item_id for r in requested_rooms)
    res_ids = set(r.biz_item_id for r in response_rooms)
    if req_ids != res_ids:
        missing = req_ids - res_ids
        extra = res_ids - req_ids
        raise ResponseMismatchError(
            f"요청/응답 biz_item_id 불일치: 누락={missing}, 과잉={extra}"
        )
