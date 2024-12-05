from starlette.websockets import WebSocket


async def get_user_session(ws: WebSocket) -> tuple[str, str] | tuple[None, None]:
    """
    A primitive WS user+session identification protocol.
    So that the `Session` state can persist across reconnections/tabs/etc., the client sends their user_id and session_id to the server.

    Args:
        ws: the websocket

    Returns:
        the user_id and session_id or None, None if the client sent invalid data
    """
    try:
        await ws.send_json({"type": "_REQUEST_USER_SESSION"})
        msg = await ws.receive_json()
        if msg["type"] != "_USER_SESSION":
            raise Exception("Client sent wrong message type")
        user = msg["data"]["user"]
        session = msg["data"]["session"]

        if not user or not session:
            raise Exception("Client sent invalid user or session")

        return user, session
    except Exception:
        try:
            await ws.close()
        finally:
            return None, None
