from fastapi import APIRouter, HTTPException,Body
from typing import List, Dict
import json
from app.models.relay import Relay, relays, AllRelaysResponse, ConfigureRelayResponse
from app.constants.http_responces import *
from app.services.GPIO_control import configure_relay

relay_route = APIRouter(tags=["Relay"])


@relay_route.get(
    "/relays[relay_id}",
    responses={
        200: {"model": ExampleResponseOK, "description": "Successful response"},
        404: {"model": ExampleResponseNotFound, "description": "Not Found"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    },
)
async def get_relay(relay_id: str):
    """Get the status of a relay"""
    if relay_id in relays:
        return relays[relay_id].Get_State()
    else:
        raise HTTPException(
            status_code=404, detail=f"Relay with id '{relay_id}' does not exist"
        )


@relay_route.post(
    "/relays",
    responses={
        200: {"model": ConfigureRelayResponse, "description": "Successful response"},
        400: {"model": ExampleResponseBadRequest, "description": "Bad Request"},
        404: {"model": ExampleResponseNotFound, "description": "Not Found"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    },
)
async def change_relay_state(request_body: List[Relay]):
    """Change the state of relays."""
    response = {}
    print(request_body)
    for relay_request in request_body:

        relay_id = relay_request.id
        relay_state = relay_request.state.upper()

        if relay_state not in ["ON", "OFF"]:
            error_dict = {"status_code": 400, "responce": "Invalid state. Must be either 'ON' or 'OFF'"}
            response[relay_id] = error_dict
            continue

        if relay_id in relays:
            configure_relay(relay_id, relay_state)
            relays[relay_id].state = relay_state
            relay_dict={"id":relay_id, "state":relay_state}
            response[relay_id] = relay_dict
        else:
            error_dict = {"status_code": 404, "responce": f"Relay with id '{relay_id}' does not exist"}
            response[relay_id] = error_dict

    return response



@relay_route.get(
    "/relays",
    responses={
        200: {"model": AllRelaysResponse, "description": "Successful response"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    },
)
async def get_all_relays():
    """Get status of all relays"""
    relay_status = {}
    for relay_id, relay in relays.items():
        relay_status[relay_id] = relay.Get_State()
    return relay_status
