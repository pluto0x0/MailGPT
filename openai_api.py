from openai import OpenAI
from utils import Config, Email
from mailop import MailOp
import json

class OpenAI_api:
    def __init__(self, config: Config, mailop: MailOp):
        self.cfg = config
        self.mailop = mailop
        self.client = OpenAI(api_key=self.cfg.openai_key)
        def read_json_file(filename):
            with open(filename, 'r', encoding='utf-8') as fd:
                return json.load(fd)
        self.msg = read_json_file(self.cfg.openai_msg)
        self.func = read_json_file(self.cfg.openai_func)
        self.available_functions = {
            "send_email": self.mailop.send_email,
        }
        
    def run_conversation(self, mail):
        messages = self.msg
        messages.append(
            {
                "role": "assistant",
                "content": repr(mail)
            }
        )
        response = self.client.chat.completions.create(
            model=self.cfg.openai_model,
            messages=messages,
            # tools=self.func,
            # tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        return response_message
'''
        tool_calls = response_message.tool_calls
        if tool_calls:
            # Note: the JSON response may not always be valid; be sure to handle errors
            while True:
                res = input('I want to call functions. Proceed? [y/n]: ').strip().lower()
                if res == 'n':
                    print('Abort.')
                    return
                elif res == 'y':
                    break
                else:
                    print('Enter again:')

            messages.append(response_message)  # extend conversation with assistant's reply
            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # validate function args
                if set(function_args.keys()) != set('receiver', 'subject', 'content'):
                    print(f'error: wrong arguments in calling function `{function_name}`')
                    print('arguments', function_args)
                    break

                function_response = function_to_call(
                    # receiver=[function_args.get("receiver")],
                    # subject=[function_args.get("subject")],
                    # content=[function_args.get("content")],
                    **function_args
                )

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.client.chat.completions.create(
                model=self.cfg.model,
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response
        return response_message
'''