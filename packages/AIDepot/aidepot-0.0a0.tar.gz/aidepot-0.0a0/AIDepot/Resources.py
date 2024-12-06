from enum import Enum


class Resources(Enum):
    LLM_JOB_RESULTS = 'llm/job_results'
    LLAMA3_2_3B_MESSAGE = 'llm/llama_3_2_3b/message'
    LLAMA3_2_3B_EMBEDDING = 'llm/llama_3_2_3b/embed'
    LLAMA3_1_8B_MESSAGE = 'llm/llama_3_1_8b/message'
    LLAMA3_1_8B_EMBEDDING = 'llm/llama_3_1_8b/embed'
    LLAMA3_2_VISION_11B_MESSAGE = 'llm/llama_3_2_vision_11b/message'
    LLAMA3_2_VISION_11B_EMBEDDING = 'llm/llama_3_2_vision_11b/embed'
    LLAMA3_1_NEMOTRON_51B_MESSAGE = 'llm/llama_3_1_nemotron_51b/message'
    LLAMA3_1_NEMOTRON_51B_EMBEDDING = 'llm/llama_3_1_nemotron_51b/embed'
    LLAMA3_1_NEMOTRON_70B_MESSAGE = 'llm/llama_3_1_nemotron_70b/message'
    LLAMA3_1_NEMOTRON_70B_EMBEDDING = 'llm/llama_3_1_nemotron_70b/embed'
    MISTRAL_7B_MESSAGE = 'llm/mistral_7b/message'
    MISTRAL_7B_EMBEDDING = 'llm/mistral_7b/embed'
    MIXTRAL_8x7B_MESSAGE = 'llm/mixtral_8x7b/message'
    MIXTRAL_8x7B_EMBEDDING = 'llm/mixtral_8x7b/embed'
    PIXTRAL_12B_MESSAGE = 'llm/pixtral_12b/message'
    PIXTRAL_12B_EMBEDDING = 'llm/pixtral_12b/embed'
