from agent.utils.logger_handler import logger
from agent.utils.config_handler import prompts_conf
from agent.utils.path_tool import get_abs_path


def load_prompt(prompt_path: str) -> str:
    """
    加载提示词内容
    :param prompt_path: 提示词文件路径
    :return: 提示词内容
    """
    try:
        absolute_prompt_path = get_abs_path(prompt_path)
    except KeyError as e:
        logger.error(f"[load_prompt] {e}")
        raise e

    try:
        return open(absolute_prompt_path, encoding='utf-8').read()
    except FileNotFoundError as e:
        logger.error(f"[load_prompt] {e}")
        raise e

def load_system_prompt() -> str:
    """
    加载系统提示词
    :return: 系统提示词
    """
    return load_prompt(prompts_conf['main_prompt_path'])

def load_rag_prompt() -> str:
    """
    加载RAG提示词
    :return: RAG提示词
    """
    return load_prompt(prompts_conf['rag_summarize_prompt_path'])

def load_report_prompt() -> str:
    """
    :return: 报告提示词
    """
    return load_prompt(prompts_conf['report_prompt_path'])


if __name__ == '__main__':
    print(load_system_prompt())