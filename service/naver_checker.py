import httpx

async def get_naver_availability(business_id, biz_item_id, date, hour_slots):
    url = "https://booking.naver.com/graphql?opName=schedule"
    start_dt = f"{date}T00:00:00"
    end_dt = f"{date}T23:59:59"

    headers = {"Content-Type": "application/json"}

    body = {
        "operationName": "schedule",
        "query": """
        query schedule($scheduleParams: ScheduleParams) {
          schedule(input: $scheduleParams) {
            bizItemSchedule {
              hourly {
                unitStartTime
                unitStock
                unitBookingCount
              }
            }
          }
        }""",
        "variables": {
            "scheduleParams": {
                "businessTypeId": 10,
                "businessId": business_id,
                "bizItemId": biz_item_id,
                "startDateTime": start_dt,
                "endDateTime": end_dt,
                "fixedTime": True,
                "includesHolidaySchedules": True
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body)
        data = response.json()

    available = {}
    for slot in data["data"]["schedule"]["bizItemSchedule"]["hourly"]:
        time_str = slot["unitStartTime"][-8:]  # e.g. "16:00:00"
        hour_min = time_str[:5]               # e.g. "16:00"
        if hour_min in hour_slots:
            available[hour_min] = slot["unitBookingCount"] < slot["unitStock"]

    return available