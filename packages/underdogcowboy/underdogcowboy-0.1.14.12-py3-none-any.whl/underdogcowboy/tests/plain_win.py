# Filename: test_agent_selected.py

from textual.app import App, ComposeResult
from textual.widgets import Label
from textual.events import Event
from textual import on
from rich.text import Text

class AgentSelected(Event):
    def __init__(self, agent_name):
        self.agent_name = agent_name
        super().__init__()

class TestApp(App):

    def compose(self) -> ComposeResult:
        # Create a Label widget and assign it to self.label for later access
        self.label = Label()
        yield self.label

    @on(AgentSelected)
    def on_agent_selected(self, event: AgentSelected):
        # Attempt to access the .plain attribute (which may not exist)
        try:
            agent_name_plain = event.agent_name.plain
            self.label.update(f"Agent name (plain): {agent_name_plain}")
        except AttributeError as e:
            self.label.update(f"Error accessing .plain: {e}")

        # Correctly extract the agent name using str()
        agent_name_str = str(event.agent_name)
        self.label.update(f"Agent name (str): {agent_name_str}")

    def on_mount(self):
        # Simulate agent selection with a Rich Text object
        agent_name_text = Text("Agent007")
        self.post_message(AgentSelected(agent_name=agent_name_text))

if __name__ == "__main__":
    app = TestApp()
    app.run()
