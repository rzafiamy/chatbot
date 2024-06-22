class ChatTemplate:
    def __init__(self, template_type="phi"):
        self.template_type = template_type
        self.templates = {
            "phi": {
                "prompt": self.phi_template,
                "response": self.phi_response
            }
        }

    def format_prompt(self, system_prompt, user_message, context):
        template = self.templates.get(self.template_type, "phi")
        return template.get("prompt", self.phi_template)(system_prompt, user_message, context)

    def format_response(self, raw_response):
        template = self.templates.get(self.template_type, "phi")
        return template.get("response", self.phi_response)(raw_response)

    #----------------- Template functions -----------------

    #------------------------------------------------------
    #  Phi template
    #------------------------------------------------------
    def phi_template(self, system_prompt, user_message, context):
        return f"<|system|>\n{system_prompt}\n<|end|>\n{context}\n\n{user_message}<|assistant|>\n"

    def phi_response(self, raw_response):
        return raw_response.split("<|assistant|>")[-1].split("<|end|>")[0].strip()