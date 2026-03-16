import os
import glob
from posixpath import join as ppjoin
from utils.save_code import save_code
from utils.sandbox_creator import create_worker
from schema.agent_state import AgentState
import logging

logger = logging.getLogger(__name__)

def execute_code(state: AgentState):
    logger.info("Executing code")
    code_list = state.get('code', [])
    latest_code = code_list[-1].content if code_list else ""
    file_name = save_code(latest_code)
    
    video_path = ""
    try:
        success, error_msg = create_worker(file_name)
        if not success:
            logger.error(f"Execution failed: {error_msg}")
            return {"execution": False, "execution_err": error_msg, "video_path": "", "file_name": file_name}
            
        from utils.save_code import get_tmp_dir
        tmp_dir = get_tmp_dir()
        script_name = file_name.replace(".py", "")
        media_videos_dir = os.path.join(tmp_dir, "code", "media", "videos", script_name, "480p15")
        
        mp4_files = glob.glob(os.path.join(media_videos_dir, "*.mp4"))
        if mp4_files:
            latest_mp4 = mp4_files[0]
            rel_path = os.path.relpath(latest_mp4, os.path.join(tmp_dir, "code", "media"))
            video_path = f"/media/{rel_path}".replace(os.path.sep, '/')
            
        return {"execution": True, "execution_err": "", "video_path": video_path, "file_name": file_name}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"execution": False, "execution_err": str(e), "video_path": "", "file_name": file_name}