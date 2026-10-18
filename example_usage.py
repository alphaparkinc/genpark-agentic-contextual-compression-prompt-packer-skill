from client import AgenticContextualPromptCompressor

def main():
    compressor = AgenticContextualPromptCompressor()
    text = """
    Enterprise compliance guidelines state all user PII must be encrypted.
    Yesterday audit logs reported 14 data leaks in the legacy MySQL database.
    Enterprise compliance guidelines state all user PII must be encrypted.
    The security team rotated all master encryption keys on AWS KMS.
    Customer verified login flow is restored.
    """
    res = compressor.compress_prompt_context(text, focus_keywords=["PII", "encryption", "AWS KMS"], target_token_budget=40)
    print("--- Contextual Compression Result ---")
    print(f"Original Tokens: ~{res['original_estimated_tokens']} | Compressed: ~{res['compressed_estimated_tokens']} (Saved: {res['compression_ratio_saved_pct']}%)")
    print(f"Compressed Output: {res['compressed_context']}")

if __name__ == "__main__":
    main()
