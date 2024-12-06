import asyncio
import os
import random
from typing import AsyncGenerator
import httpx
import pandas as pd
from loguru import logger
from skopt import Optimizer
from skopt.space import Real

from agentic_security.probe_actor.refusal import refusal_heuristic
from agentic_security.probe_data.data import prepare_prompts
from agentic_security.models.schemas import ScanResult

IS_VERCEL = os.getenv("IS_VERCEL", "f") == "t"


async def prompt_iter(prompts: list[str] | AsyncGenerator) -> AsyncGenerator[str, None]:
    if isinstance(prompts, list):
        for p in prompts:
            yield p
    else:
        async for p in prompts:
            yield p


async def perform_scan(
    request_factory,
    max_budget: int,
    datasets: list[dict[str, str]] = [],
    tools_inbox=None,
    optimize=False,
    stop_event: asyncio.Event = None,
) -> AsyncGenerator[str, None]:
    """Perform a standard security scan."""
    if IS_VERCEL:
        yield ScanResult.status_msg(
            "Vercel deployment detected. Streaming messages are not supported by serverless, please run it locally."
        )
        return

    try:
        yield ScanResult.status_msg("Loading datasets...")
        prompt_modules = prepare_prompts(
            dataset_names=[m["dataset_name"] for m in datasets if m["selected"]],
            budget=max_budget,
            tools_inbox=tools_inbox,
        )
        yield ScanResult.status_msg("Datasets loaded. Starting scan...")

        errors = []
        refusals = []
        total_prompts = sum(len(m.prompts) for m in prompt_modules if not m.lazy)
        processed_prompts = 0

        optimizer = (
            Optimizer([Real(0, 1)], base_estimator="GP", n_initial_points=25)
            if optimize
            else None
        )
        failure_rates = []

        for module in prompt_modules:
            tokens = 0
            module_failures = 0
            module_size = 0 if module.lazy else len(module.prompts)
            logger.info(f"Scanning {module.dataset_name} {module_size}")

            async for prompt in prompt_iter(module.prompts):
                if stop_event and stop_event.is_set():
                    stop_event.clear()
                    logger.info("Scan stopped by user.")
                    yield ScanResult.status_msg("Scan stopped by user.")
                    return

                processed_prompts += 1
                progress = (
                    100 * processed_prompts / total_prompts if total_prompts else 0
                )
                prompt_tokens = len(prompt.split())
                tokens += prompt_tokens

                try:
                    r = await request_factory.fn(prompt=prompt)
                    if r.status_code >= 400:
                        raise httpx.HTTPStatusError(
                            f"HTTP {r.status_code}",
                            request=r.request,
                            response=r,
                        )

                    response_text = r.text
                    response_tokens = len(response_text.split())
                    tokens += response_tokens

                    if not refusal_heuristic(r.json()):
                        refusals.append(
                            (module.dataset_name, prompt, r.status_code, response_text)
                        )
                        module_failures += 1

                except httpx.RequestError as e:
                    logger.error(f"Request error: {e}")
                    errors.append((module.dataset_name, prompt, str(e)))
                    module_failures += 1
                    continue

                failure_rate = module_failures / max(processed_prompts, 1)
                failure_rates.append(failure_rate)
                cost = round(tokens * 1.5 / 1000_000, 2)

                yield ScanResult(
                    module=module.dataset_name,
                    tokens=round(tokens / 1000, 1),
                    cost=cost,
                    progress=round(progress, 2),
                    failureRate=round(failure_rate * 100, 2),
                ).model_dump_json()

                if optimize and len(failure_rates) >= 5:
                    next_point = optimizer.ask()
                    optimizer.tell(next_point, -failure_rate)
                    best_failure_rate = -optimizer.get_result().fun
                    if best_failure_rate > 0.5:
                        yield ScanResult.status_msg(
                            f"High failure rate detected ({best_failure_rate:.2%}). Stopping this module..."
                        )
                        break

        yield ScanResult.status_msg("Scan completed.")

        df = pd.DataFrame(
            errors + refusals, columns=["module", "prompt", "status_code", "content"]
        )
        df.to_csv("failures.csv", index=False)

    except Exception as e:
        logger.exception("Scan failed")
        yield ScanResult.status_msg(f"Scan failed: {str(e)}")
        raise e


async def perform_multi_step_scan(
    request_factory,
    max_budget: int,
    datasets: list[dict[str, str]] = [],
    probe_datasets: list[dict[str, str]] = [],
    tools_inbox=None,
    optimize=False,
    stop_event: asyncio.Event = None,
    probe_frequency: float = 0.2,
) -> AsyncGenerator[str, None]:
    """Perform a multi-step security scan with probe injection."""
    if IS_VERCEL:
        yield ScanResult.status_msg(
            "Vercel deployment detected. Streaming messages are not supported by serverless, please run it locally."
        )
        return

    try:
        # Load main and probe datasets
        yield ScanResult.status_msg("Loading datasets...")
        prompt_modules = prepare_prompts(
            dataset_names=[m["dataset_name"] for m in datasets if m["selected"]],
            budget=max_budget,
            tools_inbox=tools_inbox,
        )
        probe_modules = prepare_prompts(
            dataset_names=[m["dataset_name"] for m in probe_datasets if m["selected"]],
            budget=max_budget,
            tools_inbox=tools_inbox,
        )
        yield ScanResult.status_msg("Datasets loaded. Starting scan...")

        errors = []
        refusals = []
        total_prompts = sum(len(m.prompts) for m in prompt_modules if not m.lazy)
        processed_prompts = 0
        conversation_history = {}

        optimizer = (
            Optimizer([Real(0, 1)], base_estimator="GP", n_initial_points=25)
            if optimize
            else None
        )
        failure_rates = []

        for module in prompt_modules:
            tokens = 0
            module_failures = 0
            module_size = 0 if module.lazy else len(module.prompts)
            logger.info(f"Scanning {module.dataset_name} {module_size}")
            conv_id = module.dataset_name

            async for prompt in prompt_iter(module.prompts):
                if stop_event and stop_event.is_set():
                    stop_event.clear()
                    logger.info("Scan stopped by user.")
                    yield ScanResult.status_msg("Scan stopped by user.")
                    return

                processed_prompts += 1
                progress = (
                    100 * processed_prompts / total_prompts if total_prompts else 0
                )

                # Get conversation history
                history = conversation_history.get(conv_id, [])
                full_prompt = "\n".join([*history, prompt]) if history else prompt
                prompt_tokens = len(full_prompt.split())
                tokens += prompt_tokens

                try:
                    # Main request
                    r = await request_factory.fn(prompt=full_prompt)
                    if r.status_code >= 400:
                        raise httpx.HTTPStatusError(
                            f"HTTP {r.status_code}",
                            request=r.request,
                            response=r,
                        )

                    response_text = r.text
                    response_tokens = len(response_text.split())
                    tokens += response_tokens

                    # Update history
                    history.extend([prompt, response_text])
                    history = history[-4:]  # Keep last 2 exchanges
                    conversation_history[conv_id] = history

                    if not refusal_heuristic(r.json()):
                        refusals.append(
                            (module.dataset_name, prompt, r.status_code, response_text)
                        )
                        module_failures += 1

                    # Random probe injection
                    if probe_modules and random.random() < probe_frequency:
                        probe_module = random.choice(probe_modules)
                        probe_prompts = [
                            p async for p in prompt_iter(probe_module.prompts)
                        ]
                        if probe_prompts:
                            probe = random.choice(probe_prompts)
                            full_probe = "\n".join([*history, probe])

                            probe_r = await request_factory.fn(prompt=full_probe)
                            if probe_r.status_code < 400:
                                probe_response = probe_r.text
                                tokens += len(probe.split()) + len(
                                    probe_response.split()
                                )

                                history.extend([probe, probe_response])
                                history = history[-4:]
                                conversation_history[conv_id] = history

                                if not refusal_heuristic(probe_r.json()):
                                    refusals.append(
                                        (
                                            probe_module.dataset_name,
                                            probe,
                                            probe_r.status_code,
                                            probe_response,
                                        )
                                    )
                                    module_failures += 1

                except httpx.RequestError as e:
                    logger.error(f"Request error: {e}")
                    errors.append((module.dataset_name, prompt, str(e)))
                    module_failures += 1
                    continue

                failure_rate = module_failures / max(processed_prompts, 1)
                failure_rates.append(failure_rate)
                cost = round(tokens * 1.5 / 1000_000, 2)

                yield ScanResult(
                    module=module.dataset_name,
                    tokens=round(tokens / 1000, 1),
                    cost=cost,
                    progress=round(progress, 2),
                    failureRate=round(failure_rate * 100, 2),
                ).model_dump_json()

                if optimize and len(failure_rates) >= 5:
                    next_point = optimizer.ask()
                    optimizer.tell(next_point, -failure_rate)
                    best_failure_rate = -optimizer.get_result().fun
                    if best_failure_rate > 0.5:
                        yield ScanResult.status_msg(
                            f"High failure rate detected ({best_failure_rate:.2%}). Stopping this module..."
                        )
                        break

        yield ScanResult.status_msg("Scan completed.")

        df = pd.DataFrame(
            errors + refusals, columns=["module", "prompt", "status_code", "content"]
        )
        df.to_csv("failures.csv", index=False)

    except Exception as e:
        logger.exception("Scan failed")
        yield ScanResult.status_msg(f"Scan failed: {str(e)}")
        raise e
