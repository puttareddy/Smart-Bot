from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from Client import ask_question

class EchoBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        msg = turn_context.activity.text
        response = ""
        json_response = await ask_question(question=msg)
        answer = json_response["last_answer"]
        response = str(answer)        
        return await turn_context.send_activity(
            MessageFactory.text(response)
        )