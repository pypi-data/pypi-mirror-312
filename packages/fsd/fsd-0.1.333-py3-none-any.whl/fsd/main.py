import json
import os
from fsd.coding_agent.ControllerAgent import ControllerAgent  # Ensure this module is correctly imported and available
from fsd.Deployment.DeploymentCheckAgent import DeploymentCheckAgent  # Ensure this module is correctly imported and available
from fsd.repo import GitRepo
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)
max_tokens = 4096

async def start(project_path):
    try:
        # check project_path exist
        if not os.path.exists(project_path):
            logger.error(f"Project path does not exist: {project_path}")
            raise FileNotFoundError(f"{project_path} does not exist.")

        logger.info("Initializing agents")
        repo = GitRepo(project_path)
        coding_controller = ControllerAgent(repo)
        deploy = DeploymentCheckAgent(repo)

        while True:
            user_prompt_json = input("Enter your prompt (type 'exit' to quit): ")
            if user_prompt_json.startswith('/rollback'):
                logger.info("Rollback requested")
                repo.reset_previous_commit()
                logger.info("Rollback completed")
                continue
            user_prompt, name_subdomain, tier, file_attachments, focused_files, domain, snow_mode = parse_initial_payload(user_prompt_json, project_path)


            if user_prompt == "deploy_to_server":
                logger.info("Deployment requested")
                check_result = await deploy.get_deployment_check_plans()
                logger.debug(f"Deployment check result: {check_result}")
                result = check_result.get('result')
                if result == "0" or result == 0:
                    logger.info("#### This project is not supported to deploy now!")
                    logger.info("-------------------------------------------------")
                    logger.info("#### Something went wrong, but we've reverted the changes. Please try again. Thank you for choosing us!")
                elif result == "1" or result == 1:
                    logger.info(" #### This project is eligible for deployment. `Deploy Agent` is proceeding with deployment now.")
                    path = check_result.get('full_project_path')
                    logger.info(f"Deployment path: {path}")
                    if path != "null":
                        project_type = check_result.get('project_type')
                        logger.info(f"Deploying project type: {project_type}")
                        repo.deploy_to_server(path, domain, name_subdomain, project_type)
                        logger.info(f"#### Your project is now live! Click [HERE](https://{name_subdomain}.{domain}) to visit.")
                        logger.info("#### Deployment successful!")
                        logger.info("-------------------------------------------------")
                        logger.info("#### `All done!` Keep chatting with us for more help. Thanks for using!")
                    else:
                        logger.info("#### Unable to deploy, please try again!")
                        logger.info("-------------------------------------------------")
                        logger.info("#### `All done!` Keep chatting with us for more help. Thanks for using!")

            else:
                repo.set_commit(user_prompt)
                logger.info("Starting coding controller")
                await coding_controller.get_started(user_prompt, tier, file_attachments, focused_files, snow_mode)
                logger.info("#### `All done!` Keep chatting with us for more help. Thanks for using!")
    except FileNotFoundError as e:
        logger.error(f" FileNotFoundError: {str(e)}")
        logger.info("#### Something went wrong, but we've reverted the changes. Please try again. Thank you for choosing us!")
    except EOFError:
        logger.info("#### We've safely undone everything. Feel free to prompt us with your needs!")
    except Exception as e:
        logger.error(f" Unexpected error: {str(e)}")
        logger.info("#### Something went wrong, but we've reverted the changes. Please try again. Thank you for choosing us!")

def parse_initial_payload(user_prompt_json, project_path):
    try:
        # Try to parse JSON
        data = json.loads(user_prompt_json)
        
        # Validate required fields with default values
        user_prompt = str(data.get("prompt", ""))
        file_path = list(data.get("file_path", []))
        tracked_file = list(data.get("tracked_file", []))
        name_subdomain = str(data.get("name_subdomain", "NOT_SET"))
        domain = str(data.get("domain", "NOT_SET"))
        tier = str(data.get("tier", "Free"))
        snow_mode_str = str(data.get("snow_mode", "false"))
        snow_mode = snow_mode_str.lower() == "true"

        # Process tracked files if they exist
        if tracked_file:
            tracked_file = [os.path.join(project_path, file.lstrip('./')) for file in tracked_file]

        return user_prompt, name_subdomain, tier, file_path, tracked_file, domain, snow_mode
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON input: {e}")
        # Return default values if JSON parsing fails
        return user_prompt_json, "NOT_SET", "Free", [], [], "NOT_SET", False
