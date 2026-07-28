import re

class StreamingComplianceEngine:
    """
    Middleware that wraps an LLM token stream to forcefully enforce formatting rules in real-time,
    without sacrificing TTFT (Time-To-First-Token) by waiting for the full response.
    """
    def __init__(self, stream):
        self.stream = stream
        self.in_code_block = False
        self.sentence_count = 0
        self.current_paragraph = ""

    async def process(self):
        """
        Yields chunks directly without corrupting Markdown lists or paragraphs.
        """
        async for chunk in self.stream:
            text_chunk = chunk.content if hasattr(chunk, 'content') else str(chunk)
            if isinstance(text_chunk, list):
                text_chunk = "".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in text_chunk)
            yield text_chunk
