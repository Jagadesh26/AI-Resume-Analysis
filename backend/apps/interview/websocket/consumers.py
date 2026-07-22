import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.interview.expections import InterviewException
from apps.interview.services.interview_builder import InterviewService



logger = logging.getLogger(__name__)




class InterviewConsumer(AsyncWebsocketConsumer):

    async def handle_start_interview(self, data):

        try:
            result = await self.start_interview(data)
        except (InterviewException, ValueError) as exc:
            await self.send_error(str(exc))
            return

        await self.send_json(
            event="INTERVIEW_STARTED",
            data=result,
        )



    async def handle_submit_answer(self, data):

        try:
            result = await self.submit_answer(data)
        except (InterviewException, ValueError) as exc:
            await self.send_error(str(exc))
            return

        if result["completed"]:
            await self.send_json(
                event="INTERVIEW_COMPLETED",
                data=result,
            )
            return
        await self.send_json(
            event="NEXT_QUESTION",
            data=result,
        )



    async def handle_end_interview(self, data):

        try:
            result = await self.end_interview(data)
        except (InterviewException, ValueError) as exc:
            await self.send_error(str(exc))
            return

        await self.send_json(
            event="INTERVIEW_COMPLETED",
            data=result,
        )

    async def connect(self):
        """
        Accept websocket connection.
        """
        self.interview_service = InterviewService()

        await self.accept()

        logger.info("Interview websocket connected.")

    async def disconnect(self, close_code):
        logger.info(
            "Interview websocket disconnected. Code=%s",
            close_code
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive all websocket events.
        """

        try:
            payload = json.loads(text_data)

            event = payload.get("event")

            data = payload.get("data") or payload

            if event == "START_INTERVIEW":

                await self.handle_start_interview(data)

            elif event == "SUBMIT_ANSWER":

                await self.handle_submit_answer(data)

            elif event == "END_INTERVIEW":

                await self.handle_end_interview(data)

            else:

                await self.send_error(
                    f"Unknown event '{event}'."
                )

        except Exception as exc:

            logger.exception(exc)

            await self.send_error(str(exc))


    @database_sync_to_async
    def start_interview(self, data):

        return self.interview_service.start_interview(

            user=self.scope.get("user"),

            uploaded_file=data["uploaded_file"],

            interview_type=data["interview_type"],

            interview_level=data["interview_level"],

            difficulty=data["difficulty"],

            total_questions=data["total_questions"],
        )
    

    @database_sync_to_async
    def submit_answer(self, data):

        conversation_id = (
            data.get("conversation_id")
            or self.scope.get("url_route", {}).get("kwargs", {}).get("conversation_id")
        )
        answer = (
            data.get("answer")
            or data.get("response")
            or data.get("message")
            or data.get("text")
            or ""
        )

        if not conversation_id:
            raise ValueError("conversation_id is required.")

        return self.interview_service.submit_answer(
            conversation_id=conversation_id,
            answer=answer,
        )
    

    @database_sync_to_async
    def end_interview(self, data):

        conversation_id = data.get("conversation_id") or self.scope.get("url_route", {}).get("kwargs", {}).get("conversation_id")

        if not conversation_id:
            raise ValueError("conversation_id is required.")

        return self.interview_service.end_interview(
            conversation_id=conversation_id,
        )
    

    async def send_json(
    self,
    event: str,
    data: dict,
    ):

        await self.send(
            text_data=json.dumps(
                {
                    "event": event,
                    "data": data,
                }
            )
        )


    async def send_error(self, message):
        await self.send_json(
            event="ERROR",
            data={
                "message": message,
            },
        )
