# Filename: test_agent_selected.py

from textual.app import App, ComposeResult
from textual.widgets import Label
from textual.events import Event
from textual import on

class AgentSelected(Event):
    def __init__(self, agent_name):
        self.agent_name = agent_name
        super().__init__()

class TestApp(App):

    def compose(self) -> ComposeResult:
        # Create a label to display the results
        self.result_label = Label()
        yield self.result_label

    @on(AgentSelected)
    def on_agent_selected(self, event: AgentSelected):
        outputs = []

        # Method 1: Try accessing event.agent_name.plain
        try:
            agent_name_plain = event.agent_name.plain
            outputs.append(f"event.agent_name.plain: {agent_name_plain}")
        except AttributeError as e:
            outputs.append(f"event.agent_name.plain failed: {e}")

        # Method 2: Try accessing event.agent_name.text
        try:
            agent_name_text = event.agent_name.text
            outputs.append(f"event.agent_name.text: {agent_name_text}")
        except AttributeError as e:
            outputs.append(f"event.agent_name.text failed: {e}")

        # Method 3: Try using str(event.agent_name)
        agent_name_str = str(event.agent_name)
        outputs.append(f"str(event.agent_name): {agent_name_str}")

        # Display the outputs in the label
        self.result_label.update('\n'.join(outputs))

    def on_mount(self):
        # Simulate agent_name as it might be in your application
        # For example, if agent_name is a Label widget
        agent_label = Label("Agent007")
        self.post_message(AgentSelected(agent_name=agent_label))

if __name__ == "__main__":
    app = TestApp()
    app.run()
