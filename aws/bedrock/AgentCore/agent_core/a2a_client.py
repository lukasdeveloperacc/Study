from a2a.client import A2AClient
from typing import Any
from uuid import uuid4
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    # SendStreamingMessageRequest,
)

import httpx


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        client = A2AClient(httpx_client=httpx_client, url='http://localhost:8000')
        id = uuid4().hex
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'how much is 10 USD in INR?'}
                ],
                'messageId': id,
            },
        }
        request = SendMessageRequest(id=id,
            params=MessageSendParams(**send_message_payload)
        )

        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))

        # streaming_request = SendStreamingMessageRequest(
        #     id=id,
        #     params=MessageSendParams(**send_message_payload)
        # )

        # stream_response = client.send_message_streaming(streaming_request)
        # async for chunk in stream_response:
        #     print(chunk.model_dump(mode='json', exclude_none=True))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())

