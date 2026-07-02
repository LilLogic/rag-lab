"""
A module to use and test the LLM or LLM-related functions.
"""

from src.llm.tag_extractor import extract_tags

text = """Caching improves system performance by storing frequently accessed data closer to the computation layer. However, maintaining cache consistency introduces complexity because cached data may become stale when underlying source data changes.

Time-based expiration is one of the simplest invalidation strategies. Cached entries automatically expire after a predefined duration, forcing subsequent requests to refresh data from the source system. This approach is easy to implement but may temporarily serve outdated information.

Write-through caching updates both the cache and underlying storage simultaneously during write operations. This improves consistency but may increase write latency because cache synchronization becomes part of the critical execution path.

More advanced systems use event-driven invalidation where updates trigger targeted cache eviction notifications across distributed nodes. Large-scale applications often combine multiple invalidation strategies to balance freshness, complexity, and infrastructure efficiency."""

response = extract_tags(text=text)

print(response)
