class Context:
    def __init__(self):
        # Initialize the context with an empty list for messages
        self.messages = []

    def add_message(self, role, content):
        """Add a message to the context."""
        self.messages.append({"role": role, "content": content})

    def add_function(self, role, function_name, content):
        """Add a function to the context."""
        self.messages.append({"role": role, "name": function_name, "content": content})

    def get_last_message(self, role=None):
        """Retrieve the last message, optionally filtered by role."""
        if role:
            for message in reversed(self.messages):
                if message["role"] == role:
                    return message
        else:
            return self.messages[-1] if self.messages else None

    def clear_messages(self):
        """Clear all messages in the context."""
        self.messages = []

    def get_messages(self):
        """Retrieve all messages."""
        return self.messages

    def merge_context(self, context):
        """Merge the context with another context."""
        self.messages.extend(context.get_messages())

    def __str__(self):
        return str(self.messages)
