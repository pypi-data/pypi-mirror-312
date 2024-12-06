from interlogue import Mind  # Assuming the Mind class is saved in a file named mind.py

# Define the REST and Socket URLs for the environment
HOST = "127.0.0.1"
PORT = 5001

def main():
    # Initialize the Mind with REST URL
    mind = Mind(host=HOST, port=PORT)

    # Passive Perception
    print("Passive Perception:")
    print(f"Observation: {mind.perception.observe()}")
    print(f"Hearing: {mind.perception.hear()}")

    # Active Perception: These events will trigger when the corresponding data is emitted by the server
    print("Active Perception:")
    # No explicit call for see and listen; these rely on the server to emit events.

    # Example: Interaction
    print("Interacting:")
    mind.interaction.talk("Hello, world!")
    mind.interaction.move(5, 10, strides=3)
    mind.interaction.orient(90)

    # Start the Mind server
    print("Starting the Mind...")
    mind.run()

if __name__ == "__main__":
    main()

