import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class ShortIdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()


    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()
        system_prompt = (
            f"As a senior {role}, provide a concise, specific plan:\n\n"
            "File Updates\n"
            f"- {self.repo.get_repo_path()}/path/to/file1.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n"
            f"- {{self.repo.get_repo_path()}}/path/to/file2.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n\n"
            "New Files (only if file doesn't exist)\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file1.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file2.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n\n"
            "Directory Structure (MANDATORY - ONLY for new files being added or files being moved):\n"
            "```plaintext\n"
            "project_root/\n"
            "├── path/                         # Only show directories containing new/moved files\n"
            "│   └── to/\n"
            "│       ├── new_file1.ext         # New file\n"
            "│       └── new_file2.ext         # New file\n"
            "└── new_location/                 # Only if files are being moved\n"
            "    └── moved_file.ext            # Moved from: old/path/moved_file.ext\n"
            "```\n"
            "IMPORTANT: Tree structure is MANDATORY but ONLY for:\n"
            "- New files being created\n" 
            "- Files being moved (must show source and destination)\n"
            "DO NOT include existing files that are only being modified in the tree.\n"
            "DO NOT include any files/directories not directly involved in additions/moves.\n\n"
            "Context Support:\n"
            "If context files are provided, briefly mention:\n"
            f"- Context support file: {self.repo.get_repo_path()}/path/to/context_file.ext\n"
            "- Relevant matter: [brief description of relevant information]\n"
            "Use this context to inform your plan, but do not modify context files.\n"
            "Note: If no new files need to be created, omit the 'New Files' section.\n"
            "API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API. JUST SPECIFY EXACTLY THE PURPOSE OF USING THE API AND WHERE TO USE IT.\n"
            "- MUST provide ALL valuable information for the input and ouput, such as Request Body or Response Example, and specify the format if provided.\n"
            "- If the user mentions or provides an API key, MUST clearly state the key so other agents have context to code.\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.openweathermap.org/data/2.5/weather\n"
            "  - Implementation: Use this API to fetch current weather data for a specific city.\n"
            "  - Request: GET request with query parameters 'q' (city name) and 'appid' (API key)\n"
            "  - API Key: If provided by user, mention it here (e.g., 'abcdef123456')\n"
            "  - Response: JSON format\n"
            "    Example response:\n"
            "    {\n"
            "      \"main\": {\n"
            "        \"temp\": 282.55,\n"
            "        \"humidity\": 81\n"
            "      },\n"
            "      \"wind\": {\n"
            "        \"speed\": 4.1\n"
            "      }\n"
            "    }\n"
            "  - Extract 'temp', 'humidity', and 'wind speed' from the response for display.\n"
            "Asset Integration\n"
            "- Describe usage of image/video/audio assets in new files (filename, format, placement)\n"
            "- For new images: Provide content, style, colors, dimensions, purpose\n"
            "- For social icons: Specify platform (e.g., Facebook, TikTok), details, dimensions, format\n"
            "- Only propose creatable files (images, code, documents). No fonts or audio or video files.\n"

            "UI-Related Files:\n"
            "- Create corresponding style files for each UI component\n" 
            "- Specify component hierarchy and relationships\n"
            "- List required UI elements and their basic functionality\n"
            "Example:\n"
            "- For a new 'ProductList' component:\n"
            "  - Create component file and style file\n"
            "  - List required UI elements (product cards, filters, etc)\n"
            "  - Specify data display requirements\n"
            "- For a new 'contact' page:\n"
            "  - Create page structure file and style file\n"
            "  - List form fields and validation rules\n"
            "  - Specify layout requirements\n\n"

            "Dependencies Required (Only if task requires dependencies):\n"
            "For each file that requires dependencies, specify:\n"
            f"- {self.repo.get_repo_path()}/file_path:\n"
            "  - Existing Dependencies (if found in requirements.txt, package.json, etc):\n"
            "    - dependency_name: Explain specific usage in this file\n"
            "  - New Dependencies (if not found in any dependency files):\n"
            "    - dependency_name: Explain why needed and specific usage\n"
            "    - Version (only if specific version required)\n"
            "Note: Skip this section if task has no dependency requirements\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Project Setup and Deployment:\n"
            "Enforce a deployable setup following these standard project structures:\n"

            "1. HTML/CSS Project:\n"
            "my-html-project/\n"
            "├── index.html            # Root HTML file\n"
            "├── css/\n"
            "│   └── styles.css        # Main stylesheet\n"
            "├── js/\n"
            "│   └── script.js         # JavaScript file(s) for interactions\n"
            "└── assets/\n"
            "    ├── images/           # Image assets\n"
            "    └── fonts/            # Font files\n"
            "Rules:\n"
            "- index.html should always be at the root level.\n"
            "- css/, js/, and assets/ should be organized for easy asset referencing.\n"
            "- Minify files (optional for production) for faster loading.\n"

            "2. React Project:\n"
            "my-react-project/\n"
            "├── public/\n"
            "│   ├── index.html         # Root HTML file\n"
            "│   └── favicon.ico        # Optional icon\n"
            "├── src/\n"
            "│   ├── App.js             # Main App component\n"
            "│   ├── index.js           # Entry point for React DOM rendering\n"
            "│   └── components/        # Folder for reusable components\n"
            "├── package.json           # Dependencies and scripts\n"
            "└── .gitignore             # Files to ignore in version control\n"
            "Rules:\n"
            "- package.json is required at the root for React projects.\n"
            "- public/index.html acts as the single HTML template.\n"
            "- Organize src/components/ for reusable components.\n"
            "- Use build tools (e.g., Webpack or Vite) for optimal bundling and deployment.\n"

            "Ensure that the project structure adheres to these standards for easy deployment and maintenance.\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition\n"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})
        
        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""
          

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE - NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"

            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provide context. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})


        all_attachment_file_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            self.conversation_history.append({"role": "user", "content": f"User has attached these files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})


        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Provide a concise file implementation for:\n\n{user_prompt}\n\n"
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths and tree structures use the correct path separators and formatting.\n"
            f"Use clear headings (h4 ####) to organize your response.\n\n"
            f"CRITICAL: Under '#### Directory Structure', you MUST provide ONE SINGLE tree structure that ONLY shows:\n"
            f"1. New files being added\n" 
            f"2. Files being moved from one location to another\n"
            f"DO NOT include any other files in the tree, even if they are being modified.\n"
            f"DO NOT duplicate folders or files in the tree structure.\n"
            f"VERIFY all paths are unique and clear before including them.\n"
            f"Example of CORRECT tree structure:\n"
            f"```plaintext\n"
            f"project_root/\n"
            f"├── src/                          # New file being added here\n"
            f"│   └── new_feature/\n"
            f"│       └── new_file.py           # New file\n"
            f"└── new_location/                 # File being moved here\n"
            f"    └── moved_file.py             # Moved from old location\n"
            f"```\n"
            f"INCORRECT tree structure examples:\n"
            f"- Including duplicate folders/paths\n"
            f"- Including files just being modified\n"
            f"- Having unclear or ambiguous paths\n"
            f"- Multiple trees for different purposes\n"
            f"Show complete paths for all affected files with action but not inside tree.\n\n"
            f"IMPORTANT: If any dependencies need to be installed or project needs to be built/run, provide ONLY the necessary bash commands for {platform.system()} OS:\n"
            f"```bash\n"
            f"# Only include dependency/build/run commands if absolutely required\n"
            f"# Commands must be 100% valid for {platform.system()} OS\n"
            f"```\n"
            f"IMPORTANT: THIS IS A NO-CODE PLANNING PHASE. DO NOT INCLUDE ANY ACTUAL CODE OR IMPLEMENTATION DETAILS.\n"
            f"Exclude: navigation, file opening, verification, and non-coding actions. "
            f"KEEP THIS LIST AS SHORT AS POSSIBLE, FOCUSING ON KEY TASKS ONLY. "
            f"PROVIDE FULL PATHS TO FILES THAT NEED MODIFICATION OR CREATION. "
            "FOR EACH FILE THAT NEEDS TO BE WORKED ON, WHETHER NEW, EXISTING, OR IMAGE, BE CLEAR AND SPECIFIC. MENTION ALL DETAILS, DO NOT PROVIDE ASSUMPTIONS, GUESSES, OR PLACEHOLDERS.\n"
            "WHEN MOVING A FILE, MENTION DETAILS OF THE SOURCE AND DESTINATION. WHEN ADDING A NEW FILE, SPECIFY THE EXACT LOCATION.\n"
            "VERIFY ALL PATHS ARE UNIQUE - DO NOT LIST THE SAME FILE OR FOLDER MULTIPLE TIMES.\n"
            "ONLY LIST FILES AND IMAGES THAT ARE 100% NECESSARY AND WILL BE DIRECTLY MODIFIED OR CREATED FOR THIS SPECIFIC TASK. DO NOT INCLUDE ANY FILES OR IMAGES THAT ARE NOT ABSOLUTELY REQUIRED.\n"
            "IMPORTANT: For each file, clearly state if it's new or existing related for this task only. This is crucial for other agents to determine appropriate actions.\n"
            "For paths with spaces, preserve the original spaces without escaping or encoding.\n"
            "PERFORM A COMPREHENSIVE ANALYSIS:\n"
            "- Validate all file paths and dependencies\n"
            "- Ensure all components are properly integrated\n" 
            "- Verify the implementation meets all requirements\n"
            "- Check for potential conflicts or issues\n"
            "- Ensure no duplicate paths or unclear locations\n"
            f"REMEMBER: THIS IS STRICTLY A PLANNING PHASE - NO CODE OR IMPLEMENTATION DETAILS SHOULD BE INCLUDED.\n"
            f"DO NOT PROVIDE ANYTHING EXTRA SUCH AS SUMMARY OR ANYTHING REPEAT FROM PREVIOUS INFORMATION, NO YAPPING. "
            f"Respond in: {original_prompt_language}"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
