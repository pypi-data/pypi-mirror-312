from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging

from textual import on
from textual.app import ComposeResult
from textual.widgets import Static, Button, LoadingIndicator, Label

# LLM
from agent_llm_handler import send_agent_data_to_llm  
from llm_call_manager import LLMCallManager

# Events
from events.llm_events import LLMCallComplete, LLMCallError

# UI / Session
from ui_components.session_dependent import SessionDependentUI

class FeedbackOutputUI(SessionDependentUI):
    """A UI for getting feedback from the underlying agent on how it understands 
       the structure of the output it produces."""
    
    def __init__(self, session_manager, screen_name,
                    agent_name_plain):
        super().__init__(session_manager, screen_name, agent_name_plain)
        self.session_manager = session_manager
        self.llm_call_manager = LLMCallManager()
        self.llm_call_manager.set_message_post_target(self)
        logging.info(f"post target message set to: {self.llm_call_manager._message_post_target}")


    def compose(self) -> ComposeResult:
        yield Label("Feedback on Output Structure:", id="feedback-output-label", classes="hidden")
        yield Static(id="feedback-output-result", classes="feedback-result hidden")
        yield Button("Start Feedback", id="start-feedback-output-button", classes="hidden")
        yield Button("Re-run Feedback", id="rerun-feedback-output-button", classes="hidden")
        yield LoadingIndicator(id="loading-feedback-output", classes="hidden")
    
    def on_mount(self) -> None:
        self.check_existing_feedback()
    
    def check_existing_feedback(self) -> None:
        existing_feedback = self.session_manager.get_data("last_feedback_output")
        if existing_feedback:
            self.show_feedback(existing_feedback)
            self.query_one("#rerun-feedback-output-button").remove_class("hidden")
        else:
            self.query_one("#start-feedback-output-button").remove_class("hidden")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ["start-feedback-output-button", "rerun-feedback-output-button"]:
            self.run_feedback()
    
    def run_feedback(self) -> None:
        self.query_one("#start-feedback-output-button").add_class("hidden")
        self.query_one("#rerun-feedback-output-button").add_class("hidden")
        self.query_one("#feedback-output-result").add_class("hidden")
        self.query_one("#loading-feedback-output").remove_class("hidden")

        llm_config = self.app.get_current_llm_config()
        if not llm_config:
            self.show_error("No LLM configuration available.")
            return

        current_agent = self.agent_name_plain
        if not current_agent:
            self.show_error("No agent currently loaded. Please load an agent first.")
            return

        logging.info("sending from feedback_output_ui to the LLMCallManager.")

        pre_prompt = "Provide feedback on how the following agent understands the structure of the output it produces."
      
        session_name = str(self.session_manager.current_session_name)
        asyncio.create_task(self.llm_call_manager.submit_llm_call_with_agent( 
            
            llm_function = send_agent_data_to_llm,
            llm_config = llm_config,
            session_name=session_name,
            agent_name = current_agent,
            agent_type = "clarity",
            input_id = "feedback-output",
            pre_prompt = pre_prompt,    
            post_prompt = None
             
         ))

    @on(LLMCallComplete)
    async def on_feedback_input_complete(self, event: LLMCallComplete) -> None:
        if event.input_id == "feedback-output":
            self.update_and_show_feedback(event.result)
            self.query_one("#loading-feedback-output").add_class("hidden")

    @on(LLMCallError)
    async def on_feedback_input_error(self, event: LLMCallError) -> None:
        if event.input_id == "feedback-output":    
            self.show_error(event.error)
            self.query_one("#loading-feedback-output").add_class("hidden")

    def update_and_show_feedback(self, result: str) -> None:
        self.session_manager.update_data("last_feedback_output", result, screen_name=self.screen_name)
        self.show_feedback(result)

    def show_feedback(self, result: str) -> None:
        self.query_one("#loading-feedback-output").add_class("hidden")
        self.query_one("#feedback-output-label").remove_class("hidden")
        feedback_widget = self.query_one("#feedback-output-result")
        feedback_widget.update(result)
        feedback_widget.remove_class("hidden")
        self.query_one("#rerun-feedback-output-button").remove_class("hidden")

    def show_error(self, error_message: str) -> None:
        self.query_one("#loading-feedback-output").add_class("hidden")
        self.query_one("#start-feedback-output-button").remove_class("hidden")
        self.app.notify(f"Error: {error_message}", severity="error")
