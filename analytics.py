from jobs.tracker import list_applications, applications_needing_followup

INSIGHTS_PROMPT_TEMPLATE = """Based ONLY on these real statistics (do not
invent any numbers not shown here), write 2-4 short, encouraging but honest
insight sentences for a job seeker. Distinguish clearly between actual data
and any general advice.

Total applications: {total}
By status: {by_status}
Response rate (Interview+Offer / Applied+): {response_rate}%
Applications needing follow-up (7+ days, no response): {followup_count}

Return plain text, 2-4 sentences, no markdown headers.
"""


def compute_stats() -> dict:
    """
    Pure data computation, no AI — always factually accurate.
    Returns counts by status, totals, and response rate.
    """
    apps = list_applications()
    total = len(apps)

    by_status = {}
    for app in apps:
        by_status[app["status"]] = by_status.get(app["status"], 0) + 1

    applied_or_further = sum(
        by_status.get(s, 0) for s in ["Applied", "Assessment", "Interview", "Offer", "Rejected"]
    )
    positive_outcomes = by_status.get("Interview", 0) + by_status.get("Offer", 0)
    response_rate = round((positive_outcomes / applied_or_further) * 100, 1) if applied_or_further else 0.0

    followups = applications_needing_followup()

    return {
        "total_applications": total,
        "by_status": by_status,
        "response_rate_percent": response_rate,
        "interviews": by_status.get("Interview", 0),
        "offers": by_status.get("Offer", 0),
        "rejected": by_status.get("Rejected", 0),
        "needs_followup": followups,
    }


def generate_ai_insights(manager, stats: dict = None) -> str:
    """
    Optional narrative layer on top of compute_stats(). The AI only narrates
    numbers we computed ourselves — it cannot invent statistics because the
    real numbers are injected directly into the prompt.
    """
    stats = stats or compute_stats()
    prompt = INSIGHTS_PROMPT_TEMPLATE.format(
        total=stats["total_applications"],
        by_status=stats["by_status"],
        response_rate=stats["response_rate_percent"],
        followup_count=len(stats["needs_followup"]),
    )
    system_prompt = (
        "You are CareerPilot AI's analytics narrator. You ONLY discuss the "
        "numbers given to you. You never invent statistics or claim data "
        "that wasn't provided."
    )
    return manager.generate(prompt, system_prompt=system_prompt, max_tokens=300).strip()
