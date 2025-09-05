#!/usr/bin/env python3
"""
Launch script for AirlineNexus Streamlit UI
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    try:
        print("🚀 Launching AirlineNexus Streamlit UI...")
        print("📍 URL: http://localhost:8501")
        print("💡 Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light",
            "--theme.primaryColor", "#3b82f6"
        ])
        
    except KeyboardInterrupt:
        print("\n✅ AirlineNexus UI stopped successfully!")
    except FileNotFoundError:
        print("❌ Error: Streamlit is not installed!")
        print("💡 Install with: pip install streamlit")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

if __name__ == "__main__":
    main()