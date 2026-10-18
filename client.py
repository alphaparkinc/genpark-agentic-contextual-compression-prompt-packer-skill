"""
Agentic Contextual Compression Prompt Packer (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
from typing import Dict, Any, List, Optional

class AgenticContextualPromptCompressor:
    def __init__(self, compressor_name: str = "GenPark-ContextPacker-Core"):
        self.compressor_name = compressor_name

    def compress_prompt_context(self, raw_text: str, focus_keywords: Optional[List[str]] = None, target_token_budget: int = 500) -> Dict[str, Any]:
        keywords = set([k.lower() for k in (focus_keywords or [])])
        sentences = [s.strip() for s in re.split(r'[\n\.\?!]+', raw_text) if s.strip()]
        
        scored_sentences = []
        seen_hashes = set()
        
        for idx, sent in enumerate(sentences):
            low = sent.lower()
            # De-duplicate near-identical phrases
            sent_norm = re.sub(r'\s+', ' ', low)
            if sent_norm in seen_hashes:
                continue
            seen_hashes.add(sent_norm)
            
            # Score sentence: density of keywords + position primacy
            kw_hits = sum(1 for kw in keywords if kw in low)
            primacy_weight = 1.0 / (1.0 + 0.05 * idx)
            score = (kw_hits * 3.0) + primacy_weight
            
            approx_tokens = len(sent.split()) * 1.3
            scored_sentences.append((score, idx, sent, approx_tokens))
            
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        
        selected = []
        running_tokens = 0
        for score, orig_idx, sent, tokens in scored_sentences:
            if running_tokens + tokens > target_token_budget and selected:
                continue
            selected.append((orig_idx, sent))
            running_tokens += tokens
            
        # Re-order chronologically to preserve discourse flow
        selected.sort(key=lambda x: x[0])
        compressed_text = ". ".join([s[1] for s in selected]) + "."
        
        orig_tokens_est = int(len(raw_text.split()) * 1.3)
        comp_tokens_est = int(running_tokens)
        reduction_pct = round(max(0.0, (1.0 - (comp_tokens_est / max(1, orig_tokens_est))) * 100.0), 1)
        
        return {
            "compressor": self.compressor_name,
            "original_estimated_tokens": orig_tokens_est,
            "compressed_estimated_tokens": comp_tokens_est,
            "compression_ratio_saved_pct": reduction_pct,
            "compressed_context": compressed_text,
            "retained_sentence_count": len(selected),
            "verdict": "PROMPT_CONTEXT_COMPRESSED"
        }
