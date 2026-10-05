# free-chatBot
📖 free-chatBot — User Guide
This application is a modern, dark-themed desktop AI chat assistant. It automatically fetches and lets you chat with frontier AI models completely for free by connecting to the OpenRouter API.
Because this application is packaged as a single standalone executable, you do not need Python or any special code libraries installed on your computer to run it.

🔑 Step 1: Get Your Free OpenRouter API Key
Before opening the app, you need an API key from OpenRouter. OpenRouter safely connects your computer to hundreds of public AI models.
1. Create a Free Account:
	• Open your web browser and go to https://openrouter.ai.
	• Click Sign Up in the top right corner.
	• You can sign up instantly using an existing Google account, GitHub account, or your email.
2. Generate Your Key:
	• Once logged into your dashboard, click on API Keys in the left-hand sidebar menu.
	• Click the Create Key button.
	• Give your key a nickname (for example: MyDesktopChatbot) so you know what it belongs to.
3. Copy Your Key:
	• Copy the secret key displayed on your screen immediately (it will start with sk-or-v1-...).
	• ⚠️ Note: Never share this key with anyone. It acts as your private password to access the AI models.

🚀 Step 2: Running the Application
1. Launch the Executable:
	• Double-click the compiled application file (e.g., DB-openrouter-custom-tkinter or its corresponding .exe / Linux binary filename) to launch it.
2. The First-Time Activation Check:
	• On your very first launch, the application will detect that it doesn't have a valid API key yet.
	• The main chat interface will temporarily hide, and a secure overlay window titled "API Key Expired or Invalid" will prompt you for your credentials.
3. Pasting and Activating:
	• Paste your copied sk-or-v1-... key directly into the input field.
	• Click the Validate & Save button.
4. Automatic Saving:
	• The app instantly tests your key against OpenRouter’s live servers.
	• Once confirmed valid, it automatically creates a hidden configuration file (.env) in the exact same folder as the app to remember your key.
	• 💡 The popup will close, and the main chat window will unlock. Every time you open the app in the future, it will skip this screen entirely!

💬 Step 3: Navigating the Interface
Using the application is split into three simple areas:
• Select Your Free AI Model (Top Left):
	• Click the dropdown box at the top left of the screen. The app automatically downloads a live list of every model currently offered for free on OpenRouter.
	• You can change models instantly at any point during a conversation to compare different AI answers.
• Chatting (Bottom):
	• Type your questions or prompts into the input box at the bottom of the screen.
	• Press Enter on your keyboard or click the Send button.
	• Your text pops up instantly, and the app safely fetches the AI's response in the background without freezing the window.
• Start a New Session (Top Right):
	• Click the red New Session button if you want to wipe the window clear or switch to a completely separate topic.
	• This completely clears out the visual text box and resets the AI's memory, ensuring past conversations don't confuse your new prompts.

🛠️ Troubleshooting
• The App won't launch or says "Failed to fetch models" on startup:
	• Make sure your computer is connected to the internet. The app needs an active connection to talk to OpenRouter and download the free models list.
• The AI constantly responds with "Error: ..." text:
	• Your API key might have been deleted from your OpenRouter online dashboard, or its internal status expired. To reset it, simply close the app, delete the tiny hidden .env file generated in the application's folder, and reopen the app to paste a fresh key.
