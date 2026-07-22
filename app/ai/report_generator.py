import logging
from typing import Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_community.llms import FakeListLLM

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Generates case investigation summaries from raw text/data using LangChain.
    """
    def __init__(self, llm=None):
        # Default to a mock LLM if none provided
        if llm is None:
            self.llm = FakeListLLM(responses=["[Automated Summary] This case investigation indicates..."])
        else:
            self.llm = llm
            
        # Define the prompt template for summarization
        template = (
            "You are a professional law enforcement AI assistant.\n"
            "Generate a structured case investigation summary from the provided data.\n\n"
            "Case Data:\n{case_data}\n\n"
            "Raw Notes/Text:\n{raw_text}\n\n"
            "Output the summary with the following sections: Overview, Key Entities, Timeline, and Recommended Actions."
        )
        self.prompt = PromptTemplate.from_template(template)
        
        # LangChain Expression Language (LCEL) chain
        self.chain = self.prompt | self.llm

    def generate_case_summary(self, case_data: Dict[str, Any], raw_text: str) -> str:
        """
        Generates the investigation summary based on case data and raw investigation notes.
        
        Args:
            case_data: Structured data related to the case (e.g., case ID, date, location).
            raw_text: Unstructured notes, witness testimonies, or officer reports.
            
        Returns:
            A string containing the formatted summary.
        """
        logger.info(f"Generating case summary for case: {case_data.get('case_id', 'Unknown')}")
        try:
            # Run the LCEL chain
            result = self.chain.invoke({
                "case_data": str(case_data),
                "raw_text": raw_text
            })
            return result
        except Exception as e:
            logger.error(f"Error generating case summary: {e}")
            raise
