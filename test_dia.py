from src.ai.dia_model import DiaAgent
import time

def test_dia_agent():
    # Initialize the agent
    agent = DiaAgent()
    
    try:
        # Test a greeting
        print("\nTesting greeting...")
        response = agent.process_message("Hello!")
        print(f"Response: {response}")
        audio_file = agent.generate_speech(response)
        print(f"Audio saved as: {audio_file}")
        
        time.sleep(2)  # Give some time to hear the first response
        
        # Test a question about the agent
        print("\nTesting question about agent...")
        response = agent.process_message("Who are you?")
        print(f"Response: {response}")
        audio_file = agent.generate_speech(response)
        print(f"Audio saved as: {audio_file}")
        
        time.sleep(2)
        
        # Test a goodbye
        print("\nTesting goodbye...")
        response = agent.process_message("Goodbye!")
        print(f"Response: {response}")
        audio_file = agent.generate_speech(response)
        print(f"Audio saved as: {audio_file}")
        
    finally:
        # Clean up
        agent.cleanup()

if __name__ == "__main__":
    test_dia_agent() 