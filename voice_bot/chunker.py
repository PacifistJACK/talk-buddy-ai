"""
Real-Time Clause Chunker
------------------------
Splits streamed tokens from the LLM into natural sentence and phrase boundaries.
Preserves neural voice prosody and emotional cadence by avoiding mid-phrase cuts,
ensuring Azure Neural voices sound smooth, human, and authentic.
"""

import re


class RealTimeClauseChunker:
    def __init__(self):
        self.buffer = ""
        # Sentence terminators: period, exclamation, question mark, newline
        self.sentence_end = re.compile(r"([.!?\n]+)")
        # Major clause pauses: colon, semicolon, em-dash
        self.clause_pause = re.compile(r"([:;—]+)")

    def add_token(self, token: str) -> list[str]:
        """Add a token and return any completed natural sentences or clauses."""
        self.buffer += token
        ready_chunks = []

        # 1. Primary check: Full sentence boundary (. ! ? \n)
        parts = self.sentence_end.split(self.buffer)
        if len(parts) > 1:
            ready = parts[0].strip() + parts[1]
            self.buffer = "".join(parts[2:])
            if ready.strip():
                ready_chunks.append(ready)
            return ready_chunks

        # 2. Secondary check: Major clause pause (: ; —) if at least 5 words exist
        parts = self.clause_pause.split(self.buffer)
        if len(parts) > 1 and len(parts[0].strip().split()) >= 5:
            ready = parts[0].strip() + parts[1]
            self.buffer = "".join(parts[2:])
            if ready.strip():
                ready_chunks.append(ready)
            return ready_chunks

        # 3. Comma break only if clause is already comfortably long (>= 10 words)
        if "," in self.buffer:
            comma_idx = self.buffer.find(",")
            clause_candidate = self.buffer[:comma_idx + 1]
            if len(clause_candidate.strip().split()) >= 10:
                ready_chunks.append(clause_candidate.strip())
                self.buffer = self.buffer[comma_idx + 1:].lstrip()
                return ready_chunks

        return ready_chunks

    def flush(self) -> list[str]:
        """Flush any remaining tokens at the end of the response."""
        rem = self.buffer.strip()
        self.buffer = ""
        return [rem] if rem else []

