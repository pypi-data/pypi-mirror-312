from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    robot_env: str = 'local'
    robot_user: str = 'user'
    robot_password: str = 'password'
    robot_data_folder: str = './.data'
    robot_data_db_folder: str = 'vector_db'
    robot_data_db_folder_src: str = 'src'
    robot_data_db_folder_out: str = 'out'
    robot_data_db_folder_store: str = 'store'
    robot_data_db_retention_days: float = 60
    robot_task_retention_days: float = 1
    robot_cms_host: str = ''
    robot_cms_auth: str = ''
    robot_cms_db_folder: str = 'llmVectorDb'
    robot_cms_kb_folder: str ='llmKbFile'
    robot_debugger_openai_key: str = ''
    model_config = ConfigDict(
        env_file='./.env',
        extra='ignore',
        case_sensitive=False
    )

    class RuntimeOptions(BaseModel):
        def _is_multi_process() -> bool:
            """
            Checks if the application is running with multiple worker processes.

            This function inspects the command-line arguments to determine if the
            application is configured to run with more than one worker process. It
            looks for the "--workers" argument and checks if the subsequent value
            is greater than 1.
            Sample of command-line arguments:
            fastapi run main.py --port 6001 --workers 4
            uvicorn main:app --port 6001 --workers 4

            Returns:
                bool: True if the application is running with multiple worker
                      processes, False otherwise.
            """
            import sys, os
            try:
                for i, arg in enumerate(sys.argv):
                    if arg == "--workers" and i + 1 < len(sys.argv):
                        workers = int(sys.argv[i + 1])
                        if workers > 1:
                            return True
            except (ValueError, IndexError):
                pass
            # Fallback: Compare process and parent process IDs
            return False #os.getpid() != os.getppid()
        debug: bool
        loader_strategy: str
        loader_show_progress: bool
        loader_silent_errors: bool
        is_multi_process: bool = _is_multi_process()


    def runtime_options(self) -> RuntimeOptions:
      """_summary_
      Returns:
          _runtime_options:
            return degug flag and loader options based on the robot environment.
            the loader options is usefull to minimizing sytem requirements/dependencies for local development
      """
      if self.robot_env == "local":
        return self.RuntimeOptions(debug=True,loader_strategy="auto",loader_show_progress=True, loader_silent_errors=True)
      elif self.robot_env == "development":
        return self.RuntimeOptions(debug=True,loader_strategy="",loader_show_progress=True, loader_silent_errors=False)
      else:
        return self.RuntimeOptions(debug=False,loader_strategy="",loader_show_progress=False, loader_silent_errors=True)

# global instance
config = Settings()

