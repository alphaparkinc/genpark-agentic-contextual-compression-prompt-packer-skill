#!/usr/bin/env python3
import json
import sys
from client import AgenticContextualPromptCompressor

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        compressor = AgenticContextualPromptCompressor()
        raw = "User requested database connection timeout fix. The system crashed twice today. We checked PgBouncer logs. PgBouncer had connection saturation at 1000 max clients. The system crashed twice today. We restarted PgBouncer and set limit to 5000."
        res = compressor.compress_prompt_context(raw, focus_keywords=["PgBouncer", "timeout", "saturation"], target_token_budget=30)
        assert res["compression_ratio_saved_pct"] > 0.0
        assert "pgbouncer" in res["compressed_context"].lower()
        print(f"[TEST PASS] Prompt Compressor Saved: {res['compression_ratio_saved_pct']}% tokens")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-prompt-compressor", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "compress_prompt_context", "description": "Contextual token compression for LLM prompts"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                compressor = AgenticContextualPromptCompressor()
                out = compressor.compress_prompt_context(args.get("raw_text", ""), args.get("focus_keywords"), args.get("target_token_budget", 500))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
