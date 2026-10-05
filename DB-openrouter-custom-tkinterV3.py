import os
import requests
import threading
import tkinter as tk
import customtkinter as ctk
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Global pointers so they can be changed dynamically by the validation popup ---
client = None
models = {}
root = None # Placeholder, set later

# 1. Get key from .env first; temporary fallback kept for immediate testing.
#    SECURITY NOTE: Remove the fallback string and ensure it's in your .env file!
#api_key = os.getenv("OPENAI_API_KEY")
#if not api_key:
#    api_key = "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"
#    print("WARNING: Using hardcoded API key fallback. Add your key to .env and remove this line for safety.")

api_key = os.getenv("OPENAI_API_KEY", "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")

# Initial system message layout
INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}
messages = [INITIAL_SYSTEM_MESSAGE]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def save_key_to_env(new_key):
    env_file = ".env"
    lines = []
    key_updated = False

    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            if line.strip().startswith("OPENAI_API_KEY="):
                lines[i] = f'OPENAI_API_KEY="{new_key}"\n'
                key_updated = True
                break

    if not key_updated:
        lines.append(f'\nOPENAI_API_KEY="{new_key}"\n')

    with open(env_file, "w") as f:
        f.writelines(lines)
    
    print("API Key successfully written and persistent inside your .env configuration file.")

def get_free_model():
    try:
        # FIXED: Use the correct API endpoint that returns JSON data
        headers = {"Authorization": f"Bearer {api_key}"}
        data = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10).json()["data"]
        
        return {
            m["name"]: m["id"]
            for m in data
            if str(m.get("pricing", {}).get("prompt")) == "0" and str(m.get("pricing", {}).get("completion")) == "0"
        }
    except Exception as e:
        print(f"Failed to fetch models from API: {e}")
        return {}

def clear_session():
    global messages
    messages = [INITIAL_SYSTEM_MESSAGE]
    
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    chat_box.insert("end", "--- New Session Started ---\n\n")
    chat_box.configure(state="disabled")

def send_message():
    text = entry.get().strip()
    if not text:
        return
    
    # Prevent sending if no models are available
    if model_var.get() not in models:
        chat_box.configure(state="normal")
        chat_box.insert("end", "No free models available right now.\n")
        chat_box.configure(state="disabled")
        return

    entry.delete(0, "end")

    chat_box.configure(state="normal")
    chat_box.insert("end", f"You: {text}\n")
    chat_box.configure(state="disabled")

    messages.append({"role": "user", "content": text})
    threading.Thread(target=get_reply, daemon=True).start()

def _update_chat(text):
    """Safe wrapper to update the UI on the main thread."""
    try:
        chat_box.configure(state="normal")
        chat_box.insert("end", f"{text}\n\n")
        chat_box.configure(state="disabled")
        chat_box.see("end")
    except Exception as e:
        print(f"UI update error: {e}")

def get_reply():
    model_id = models[model_var.get()]
    try:
        response = client.chat.completions.create(
            model=model_id, 
            messages=messages
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        _update_chat(f"Bot: {reply}")
    except Exception as e:
        reply = f"Error: {e}"
        _update_chat(f"Bot: {reply}")

# --- Correct Expiration Check Logic ---
def check_key_validity(key_to_test):
    try:
        url = "https://openrouter.ai/api/v1/auth/key"
        headers = {"Authorization": f"Bearer {key_to_test}"}
        res = requests.get(url, headers=headers, timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def finalize_dashboard_setup():
    """Populates fallback layouts, dictionary menus, and updates the dropdown selector."""
    global models
    models = get_free_model()
    model_values = list(models.keys()) if models else ["No Free Models Found"]
    model_dropdown.configure(values=model_values)
    if models:
        model_var.set(model_values[0])
    else:
        model_var.set("No Free Models Found")

def validate_and_initialize_api():
    """Checks key validity first. Triggers popup modal if key is expired/invalid."""
    global client
    if check_key_validity(api_key):
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        finalize_dashboard_setup()
    else:
        root.withdraw()  # Temporarily hide the main dashboard until a valid key is given
        request_new_key_ui()

def request_new_key_ui():
    """Displays a modal asking the user to provide an active, unexpired OpenRouter API Key."""
    modal = ctk.CTkToplevel()
    modal.title("API Key Expired or Invalid")
    modal.geometry("450x180")
    modal.resizable(False, False)
    
    # Force modal to foreground
    modal.attributes("-topmost", True)
    modal.grab_set()

    lbl = ctk.CTkLabel(
        modal, 
        text="The current OpenRouter API Key is invalid or expired.\nPlease enter a new key to proceed:", 
        font=("Arial", 12)
    )
    lbl.pack(pady=(20, 10))

    key_entry = ctk.CTkEntry(modal, placeholder_text="sk-or-v1-...", width=380, show="*")
    key_entry.pack(pady=5)

    error_lbl = ctk.CTkLabel(modal, text="", text_color="#e74c3c", font=("Arial", 11))
    error_lbl.pack()

    def submit_key():
        global api_key, client
        input_key = key_entry.get().strip()
        
        if check_key_validity(input_key):
            api_key = input_key
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            
            # Save the key into your local directory's persistent storage file
            save_key_to_env(api_key)
            
            modal.destroy()
            root.deiconify()  # Bring back main application window
            finalize_dashboard_setup()
        else:
            error_lbl.configure(text="Validation failed. This key is also invalid or expired.")

    submit_btn = ctk.CTkButton(modal, text="Validate & Save", command=submit_key)
    submit_btn.pack(pady=(5, 10))
    
    # Destroys main thread if window closed intentionally
    modal.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

# --- Main Window Loop ---
root = ctk.CTk()
root.title("OpenRouter Chatbot (Free Models)")
root.geometry("500x550")

# --- Top Navigation / Management Bar ---
top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(fill="x", padx=10, pady=10)

# Dropdown selection element (Fixed: Removed duplicate model_var definition)
model_var = tk.StringVar(value="Verifying Connection...")
model_dropdown = ctk.CTkComboBox(top_frame, variable=model_var, values=["Checking Key Status..."])
model_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))

# Clear Session Activation Element
clear_btn = ctk.CTkButton(top_frame, text="New Session", width=100, fg_color="#c0392b", hover_color="#e74c3c", command=clear_session)
clear_btn.pack(side="right")

# --- Main Interface Areas ---
chat_box = ctk.CTkTextbox(root, wrap="word", state="disabled")
chat_box.pack(fill="both", expand=True, padx=10)

input_frame = ctk.CTkFrame(root, fg_color="transparent")
input_frame.pack(fill="x", padx=10, pady=10)

entry = ctk.CTkEntry(input_frame)
entry.pack(side="left", fill="x", expand=True)
entry.bind("<Return>", lambda e: send_message())

ctk.CTkButton(input_frame, text="Send", width=80, command=send_message).pack(
    side="right", padx=(10, 0)
)

# Run validity test immediately after the main window constructs
root.after(100, validate_and_initialize_api)

root.mainloop()
