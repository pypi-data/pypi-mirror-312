from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests


class Memory:
    """Generic memory module that allows users to choose their data structure."""
    def __init__(self, storage=None):
        self.storage = storage if storage is not None else {}

    def save(self, key, value):
        """Save data into memory."""
        self.storage[key] = value

    def retrieve(self, key):
        """Retrieve data from memory."""
        return self.storage.get(key, None)

    def delete(self, key):
        """Delete a memory."""
        if key in self.storage:
            del self.storage[key]


class Perception:
    """Handles how the Mind perceives the environment."""

    def __init__(self, socketio, rest_url=None):
        self.socketio = socketio
        self.rest_url = rest_url
        self._register_listeners()

        if not self.rest_url:
            print("Warning: REST API URL not provided. Passive perception may not work.")

    # Passive Perception via REST APIs
    def observe(self):
        """Passively perceive the environment via REST API."""
        if not self.rest_url:
            return "No REST URL provided to observe the environment."
        try:
            response = requests.get(f"{self.rest_url}/observe")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Failed to fetch environment state: {e}"

    def hear(self):
        """Passively perceive sound via REST API."""
        if not self.rest_url:
            return "No REST URL provided to hear the environment."
        try:
            response = requests.get(f"{self.rest_url}/hear")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Failed to fetch sound state: {e}"

    # Active Perception via Socket.IO Listeners
    def _register_listeners(self):
        """Register Socket.IO event listeners for active perception."""
        @self.socketio.on('see')
        def handle_see(data):
            print(f"Actively saw: {data}")

        @self.socketio.on('listen')
        def handle_listen(data):
            print(f"Actively listened to: {data}")


class Cognition:
    """Handles the cognitive abilities of the Mind."""

    @staticmethod
    def think(input_text):
        """Process an input and produce a response."""
        return f"Thinking about: {input_text}"

    @staticmethod
    def reflect(input_text):
        """Background reflection process."""
        return f"Reflecting on: {input_text}"


class Interaction:
    """Handles interactions with the environment."""

    def __init__(self, socketio):
        self.socketio = socketio

    def talk(self, message):
        """Emit a message to the environment."""
        self.socketio.emit('talk', {'message': message})

    def move(self, x, y, strides=1):
        """Move to a specific position within stride limits."""
        if strides > 5:
            strides = 5
        self.socketio.emit('move', {'x': x, 'y': y, 'strides': strides})

    def orient(self, degrees):
        """Orient the Mind to a specific angle."""
        self.socketio.emit('orient', {'angle': degrees})


class Mind:
    """A comprehensive class representing a Mind."""

    def __init__(self, host="0.0.0.0", port=5001, rest_url=None, cors_allowed_origins="*"):
        # Flask app and SocketIO setup
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": cors_allowed_origins}})
        self.socketio = SocketIO(self.app, cors_allowed_origins=cors_allowed_origins)

        # External connection URL
        self.rest_url = rest_url

        if not self.rest_url:
            print("Warning: No REST API URL provided. Passive perception will not be connected to an environment.")

        # Components
        self.memory = Memory()
        self.perception = Perception(self.socketio, self.rest_url)
        self.cognition = Cognition()
        self.interaction = Interaction(self.socketio)

        # Server configuration
        self.host = host
        self.port = port

    def run(self, debug=True):
        """Run the server."""
        print(f"Mind server running at http://{self.host}:{self.port}")
        self.socketio.run(self.app, host=self.host, port=self.port, debug=debug)
