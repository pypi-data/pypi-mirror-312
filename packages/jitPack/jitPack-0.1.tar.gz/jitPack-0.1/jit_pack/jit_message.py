import threading
from typing import Callable, Any, Optional
import logging
from fastapi import FastAPI, HTTPException
import uvicorn
from rx.subject import Subject
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Message(BaseModel):
    action: str
    order_id: str

class MessageServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI()
        self.server: Optional[uvicorn.Server] = None
        self.thread: Optional[threading.Thread] = None
        self.message_subject = Subject()

        @self.app.post("/message")
        async def receive_message(message: Message):
            try:
                # Emit the received message to all subscribers
                self.message_subject.on_next(message.model_dump())
                return {"status": "Message received"}
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

    def start_server(self) -> None:
        if self.thread and self.thread.is_alive():
            logger.warning("Server is already running.")
            return

        def run_server() -> None:
            config = uvicorn.Config(self.app, host=self.host, port=self.port)
            self.server = uvicorn.Server(config)
            try:
                self.server.run()
            except Exception as e:
                logger.error(f"Server error: {str(e)}")

        self.thread = threading.Thread(target=run_server)
        self.thread.start()
        logger.info(f"Server started on http://{self.host}:{self.port}")

    def stop_server(self) -> None:
        if self.server:
            logger.info("Stopping server...")
            self.server.should_exit = True
            if self.thread:
                self.thread.join(timeout=5)  # Wait up to 5 seconds for the thread to finish
                if self.thread.is_alive():
                    logger.warning("Server thread did not terminate within the timeout period.")
            self.server= None
            logger.info("Server stopped.")

    def subscribe(self, observer: Callable[[Any], None]) -> Any:
        return self.message_subject.subscribe(observer)


    def dispose(self) -> None:
        """Dispose of resources, stopping the server and completing the subject."""
        self.stop_server()
        self.message_subject.on_completed()