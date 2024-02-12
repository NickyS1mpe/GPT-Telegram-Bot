import os
import time
import telepot
from telepot.loop import MessageLoop
from openai import OpenAI

# Replace with the token of your Telegram bot and your API key of OpenAI
bot_token = ''
api_key = ''
current_model = 'gpt-4-0613'

# You can use your own prompt to define the personality and behavior of the AI
prompt = '''

'''

# Bot name
bot_nickname = ''
# Bot username
bot_username = '@'
# Bot statement
bot_statement = f"\n\n^*I am an auto-reply bot using {current_model}. If you want to chat with me, please mention my name {bot_nickname}*"
bot_enable = True
# Nickname of the bot in the group
group_user_nickname = ""

# Initialize bot and OpenAI services
bot = telepot.Bot(bot_token)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", f"{api_key}"))


# Build the submission context to send to AI
def build_submission_context(name, context):
    context_str = f'[system](#context)\nHere is the comment made by {name} in a group named {group_user_nickname}\n'
    if context != "":
        context_str += f", the content is “{context[:3000]}”"
    context_str += "\n\n"
    context_str += f"[system][#additional_instructions]\nWhen replying, instead of repeating or imitating what the {name} you are replying to said, you reply with your own creativity. Needn't introduce yourself. Only output the body of your reply. Do not attach the original text, do not output all possible replies."
    return context_str


# Send the message along with the reply to the original chat
def telegram_bot_sendText(bot_msg, chat_id, msg_id):
    bot.sendMessage(chat_id, bot_msg, reply_to_message_id=msg_id)
    return 'Replied'


# Send a message directly in the chat room
def telegram_bot_send(bot_msg, chat_id):
    bot.sendMessage(chat_id, bot_msg)
    return 'Replied'


# Function to interact with OpenAI and get AI response
def openAI(context):
    context = 'system\n\n' + context
    ask_string = "Please reply to the conversation."
    response = client.chat.completions.create(
        model=current_model,
        messages=[{'role': 'user', 'content': context},
                  {'role': 'system', 'content': ask_string}],
        temperature=0,
        max_tokens=200
    )
    context_reply = response.choices[0].message.content
    print(context_reply)
    return context_reply


# Main functionality of the bot
def chat_bot(msg):
    cwd = os.getcwd()
    # Timer log records the timestamp to ensure the latest message is obtained
    timer_log = cwd + '/timer_log.txt'
    global bot_enable

    # Check if the log file exists, if not, create a new one
    if not os.path.exists(timer_log):
        with open(timer_log, "w") as f:
            f.write('1')
    else:
        print("Timer Log Exists")

    with open(timer_log) as f:
        last_update = f.read()

    # Get message summary
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # If it's a text message
    if content_type == 'text':

        try:
            # If the message time is greater than the timestamp in the log, and the message is not empty
            if float(msg['date']) > float(last_update) and msg['text'] != "":
                # Non-bot messages
                if not msg['from']['is_bot']:
                    # Update the timestamp
                    last_update = str(int(msg['date']))

                    # Get the message ID and content
                    msg_id = str(int(msg['message_id']))
                    context = prompt
                    context += build_submission_context(msg['from']['first_name'] + " " + msg['from']['last_name'],
                                                        msg['text'])

                    # If the bot is enabled
                    if bot_enable:
                        # Check if the message contains a bot call
                        if f'{bot_nickname}' in msg['text'] or f'{bot_username}' in msg['text']:
                            bot_response = openAI(context)
                            print(telegram_bot_sendText(bot_response + bot_statement, chat_id, msg_id))

                        # Some simple commands. Need to be added to the bot first in Telegram.
                        # Check if the message of bot has been replied to
                        elif 'reply_to_message' in msg:
                            if msg['reply_to_message']['from']['is_bot']:
                                bot_response = openAI(f"{context}")
                                print(telegram_bot_sendText(bot_response + bot_statement, chat_id, msg_id))
                        # Return the basic info of bot
                        elif '/info' in msg['text']:
                            bot_info = bot.getMe()
                            bot_response = "I am a bot named " + f"{bot_info['first_name']}"
                            print(telegram_bot_send(bot_response + bot_statement, chat_id))
                        # Disable the bot
                        elif '/disable_bot' in msg['text']:
                            bot_enable = False
                            print(telegram_bot_send('Bot disabled', chat_id))

                    # Enable the bot
                    if '/enable_bot' in msg['text']:
                        bot_enable = True
                        print(telegram_bot_send('Bot enabled', chat_id))

        except Exception as e:
            print(e)

        # Update the timestamp in the log
        with open(timer_log, "w") as f:
            f.write(last_update)

    return "done"


# Main function
def main():
    # Continuously listen
    MessageLoop(bot, chat_bot).run_as_thread()

    print("Listening...")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    print(bot.getMe())
    main()
