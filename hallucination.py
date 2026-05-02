# hallucination.py
# Simple but effective hallucination detection
# Checks if the answer is grounded in the retrieved context

import re


# ── Confidence thresholds ─────────────────────────────────────────────────────
SIMILARITY_THRESHOLD = 0.3   # min word overlap to consider grounded
UNCERTAINTY_PHRASES  = [     # phrases that mean LLM is unsure
    "i don't know",
    "i am not sure",
    "i'm not sure",
    "i cannot",
    "i can't",
    "i don't have",
    "i do not have",
    "not enough information",
    "i don't have enough",
    "i cannot find",
    "no information",
    "unclear",
    "uncertain",
]

HALLUCINATION_RISK_PHRASES = [  # phrases that suggest made-up content
    "as of my knowledge",
    "as far as i know",
    "i believe",
    "i think",
    "probably",
    "i assume",
    "it's possible",
    "might be",
    "could be",
    "i'm guessing",
]


def clean_text(text: str) -> set:
    """
    Clean text and return set of meaningful words.
    Removes punctuation and common stop words.
    """
    stop_words = {
        "the", "a", "an", "is", "it", "in", "on", "at", "to",
        "for", "of", "and", "or", "but", "with", "by", "from",
        "that", "this", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "can",
        "not", "no", "so", "as", "if", "then", "than", "into"
    }

    # Lowercase and remove punctuation
    text  = text.lower()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)  # words 3+ chars

    # Remove stop words
    return set(w for w in words if w not in stop_words)


def check_word_overlap(answer: str, context: str) -> float:
    """
    Calculate what percentage of answer words appear in context.
    Higher overlap = more grounded in context = less hallucination.

    Returns:
        float between 0.0 (no overlap) and 1.0 (full overlap)
    """
    if not context:
        return 0.0

    answer_words  = clean_text(answer)
    context_words = clean_text(context)

    if not answer_words:
        return 0.0

    # How many answer words are in context?
    overlap       = answer_words.intersection(context_words)
    overlap_score = len(overlap) / len(answer_words)

    return round(overlap_score, 3)


def check_uncertainty(answer: str) -> dict:
    """
    Check if LLM expressed uncertainty in its answer.
    Uncertainty = honest answer = GOOD (not hallucination).

    Returns:
        dict with is_uncertain flag and phrases found
    """
    answer_lower    = answer.lower()
    found_uncertain = [p for p in UNCERTAINTY_PHRASES        if p in answer_lower]
    found_risky     = [p for p in HALLUCINATION_RISK_PHRASES if p in answer_lower]

    return {
        "is_uncertain"     : len(found_uncertain) > 0,
        "uncertainty_phrases": found_uncertain,
        "risk_phrases"     : found_risky,
        "has_risk_phrases" : len(found_risky) > 0
    }


def detect_hallucination(
    question: str,
    answer  : str,
    context : str
) -> dict:
    """
    Main hallucination detection function.
    Combines multiple checks to produce a risk score.

    Args:
        question : user's question
        answer   : LLM's answer
        context  : retrieved FAISS context

    Returns:
        dict with:
          - hallucination_risk : "LOW" / "MEDIUM" / "HIGH"
          - confidence_score   : 0.0 to 1.0 (higher = more trustworthy)
          - details            : breakdown of checks
          - warning            : human readable warning if any
    """

    details = {}

    # ── Check 1: Word overlap with context ────────────────────────────────
    overlap_score        = check_word_overlap(answer, context)
    details["overlap"]   = overlap_score
    details["context_provided"] = bool(context)

    # ── Check 2: Uncertainty phrases ──────────────────────────────────────
    uncertainty          = check_uncertainty(answer)
    details["uncertainty"] = uncertainty

    # ── Check 3: Answer length ────────────────────────────────────────────
    # Very short answers to complex questions can be suspicious
    answer_words          = len(answer.split())
    details["answer_length"] = answer_words

    # ── Check 4: Context was provided but not used ────────────────────────
    context_ignored = (
        bool(context) and
        overlap_score < SIMILARITY_THRESHOLD and
        not uncertainty["is_uncertain"]
    )
    details["context_ignored"] = context_ignored

    # ── Calculate confidence score ────────────────────────────────────────
    confidence = 0.5  # start at 50%

    # Boost if good overlap with context
    if context and overlap_score >= SIMILARITY_THRESHOLD:
        confidence += 0.3

    # Boost if LLM honestly said it doesn't know
    if uncertainty["is_uncertain"]:
        confidence += 0.2

    # Penalise if context provided but ignored
    if context_ignored:
        confidence -= 0.3

    # Penalise for risky phrases
    if uncertainty["has_risk_phrases"]:
        confidence -= 0.1

    # Penalise for very short answers
    if answer_words < 5:
        confidence -= 0.1

    # Clamp between 0 and 1
    confidence = round(max(0.0, min(1.0, confidence)), 2)

    # ── Determine risk level ──────────────────────────────────────────────
    if confidence >= 0.7:
        risk    = "LOW"
        warning = None
    elif confidence >= 0.4:
        risk    = "MEDIUM"
        warning = "⚠️  Answer may not be fully grounded in context. Verify if important."
    else:
        risk    = "HIGH"
        warning = "🚨 High hallucination risk! Answer may be unreliable. Please verify."

    return {
        "hallucination_risk": risk,
        "confidence_score"  : confidence,
        "details"           : details,
        "warning"           : warning
    }