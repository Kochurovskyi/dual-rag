"""Query expansion utilities for improving retrieval accuracy."""
import re
from typing import List


def extract_entities(query: str) -> List[str]:
    """Extract entities (capitalized terms, technical terms) from query."""
    # Extract capitalized terms (likely entities) - exclude common words
    common_words = {'What', 'How', 'When', 'Where', 'Why', 'Which', 'The', 'This', 'That', 'These', 'Those', 'I', 'You', 'We', 'They'}
    entities = re.findall(r'\b([A-Z][a-zA-Z]+)\b', query)
    entities = [e for e in entities if e not in common_words and len(e) > 2]
    
    # Also extract quoted terms
    entities.extend(re.findall(r'"([^"]+)"', query))
    
    # For "difference between X and Y" pattern, extract X and Y
    match = re.search(r'difference between (.+?) and (.+?)(?:\?|$)', query, re.IGNORECASE)
    if match:
        x, y = match.groups()
        # Extract capitalized terms from X and Y
        x_entities = re.findall(r'\b([A-Z][a-zA-Z]+)\b', x)
        y_entities = re.findall(r'\b([A-Z][a-zA-Z]+)\b', y)
        entities.extend([e for e in x_entities if e not in common_words])
        entities.extend([e for e in y_entities if e not in common_words])
    
    return list(set(entities))


def expand_query(query: str) -> List[str]:
    """
    Expand query with variations for better retrieval (Phase 3.1).
    
    Returns list of query variations including the original.
    """
    expansions = [query]  # Always include original
    query_lower = query.lower()
    
    # Comparison queries
    if "difference between" in query_lower or " vs " in query_lower or "versus" in query_lower or "compare" in query_lower:
        entities = extract_entities(query)
        if len(entities) >= 2:
            expansions.extend([
                f"{entities[0]} {entities[1]} comparison",
                f"{entities[0]} vs {entities[1]}",
                f"{entities[1]} vs {entities[0]}",  # Reverse order
                f"{entities[0]} {entities[1]} differences",
                f"compare {entities[0]} {entities[1]}",
                f"{entities[0]} {entities[1]} contrast"
            ])
        # Also try extracting from "difference between X and Y"
        match = re.search(r'difference between (.+?) and (.+?)(?:\?|$)', query_lower)
        if match:
            x, y = match.groups()
            expansions.extend([
                f"{x.strip()} {y.strip()} comparison",
                f"{x.strip()} vs {y.strip()}"
            ])
    
    # Best practices queries
    if "best practice" in query_lower:
        expansions.extend([
            query.replace("best practice", "recommendation"),
            query.replace("best practice", "guideline"),
            query.replace("best practice", "pattern"),
            query.replace("best practice", "tip"),
            query.replace("best practice", "advice")
        ])
    
    # Error handling queries
    if "error" in query_lower or "retry" in query_lower:
        expansions.extend([
            query.replace("error", "exception"),
            query.replace("retry", "retry policy"),
            query + " handling",
            query + " recovery",
            query.replace("handle", "manage")
        ])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_expansions = []
    for exp in expansions:
        exp_lower = exp.lower()
        if exp_lower not in seen:
            seen.add(exp_lower)
            unique_expansions.append(exp)
    
    return unique_expansions

