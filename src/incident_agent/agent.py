"""Google ADK entry point, discoverable with `adk web` or `adk run`."""

from google.adk.agents import Agent

from .ops_tools import calculate_error_rate, get_runbook, get_service_health

root_agent = Agent(
    name="incident_triage_agent",
    model="gemini-2.5-flash",
    description="Investigates simulated service incidents using health and runbook tools.",
    instruction="""
You are an incident-triage assistant for a simulated software company.

Your job is to gather evidence, calculate relevant metrics, and recommend safe next steps.
Always check service health before diagnosing an incident. Calculate the error rate when counts
are available. Consult the runbook for degraded services. Clearly separate observed facts from
your inference. Never claim that you performed a rollback, deployment, credential rotation, or
other production mutation. Those actions require explicit human approval and are not available
as tools. If a service is unknown, say so instead of inventing information.
""".strip(),
    tools=[get_service_health, get_runbook, calculate_error_rate],
)

