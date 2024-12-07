from homeassistant.core import HomeAssistant  # type: ignore
import logging


async def handle_security_update_feedback (hass: HomeAssistant, info: dict):
    # remove auxilary bytes which represents number of scenarios
    channels_number = info["additional_bytes"][0]
    mode = info["additional_bytes"][1]
    event_data = {
        "device_id": info["device_id"],
        "feedback_type": "security_update",
        "additional_bytes": info["additional_bytes"],
        "channel_number": channels_number,
        "mode": mode,
    }
    try:
        hass.bus.async_fire(str(info["device_id"]), event_data)
        #logging.error(f"update response event fired for {info['device_id']}")
    except Exception as e:
        logging.error(f"error in firing event: {e}")
