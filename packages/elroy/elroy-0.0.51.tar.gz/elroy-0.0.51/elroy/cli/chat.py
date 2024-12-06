import logging
from datetime import timedelta
from typing import Iterable

from colorama import init
from toolz import concat, pipe, unique
from toolz.curried import filter, map

from ..config.config import ElroyContext
from ..io.cli import CliIO
from ..messaging.messenger import process_message, validate
from ..onboard_user import onboard_user
from ..repository.data_models import SYSTEM, USER, ContextMessage
from ..repository.message import (
    get_context_messages,
    get_time_since_most_recent_user_message,
    replace_context_messages,
)
from ..repository.user import is_user_exists
from ..system_commands import SYSTEM_COMMANDS, contemplate
from ..tools.user_preferences import get_user_preferred_name, set_user_preferred_name
from ..utils.clock import get_utc_now
from ..utils.utils import run_in_background_thread
from .commands import invoke_system_command
from .context import get_completer, get_user_logged_in_message, periodic_context_refresh


async def handle_chat(context: ElroyContext[CliIO]):
    init(autoreset=True)

    run_in_background_thread(periodic_context_refresh, context)

    context.io.print_title_ruler()

    if not is_user_exists(context):
        context.io.notify_warning("Elroy is in alpha release")
        name = await context.io.prompt_user("Welcome to Elroy! What should I call you?")
        user_id = onboard_user(context.session, context.io, context.config, name)
        assert isinstance(user_id, int)

        set_user_preferred_name(context, name)
        print_memory_panel(context, get_context_messages(context))
        await process_and_deliver_msg(context, "Elroy user {name} has been onboarded. Say hello and introduce yourself.", role=SYSTEM)
        context_messages = get_context_messages(context)

    else:
        context_messages = get_context_messages(context)

        validated_messages = validate(context.config, context_messages)

        if context_messages != validated_messages:
            replace_context_messages(context, validated_messages)
            logging.warning("Context messages were repaired")
            context_messages = get_context_messages(context)

        print_memory_panel(context, context_messages)

        if (get_time_since_most_recent_user_message(context_messages) or timedelta()) < context.config.min_convo_age_for_greeting:
            logging.info("User has interacted recently, skipping greeting.")

        else:
            get_user_preferred_name(context)

            # TODO: should include some information about how long the user has been talking to Elroy
            await process_and_deliver_msg(
                context,
                get_user_logged_in_message(context),
                SYSTEM,
            )

    while True:
        try:
            context.io.update_completer(get_completer(context, context_messages))

            user_input = await context.io.prompt_user()
            if user_input.lower().startswith("/exit") or user_input == "exit":
                break
            elif user_input:
                await process_and_deliver_msg(context, user_input)
                run_in_background_thread(contemplate, context)
        except EOFError:
            break

        context.io.rule()
        context_messages = get_context_messages(context)
        print_memory_panel(context, context_messages)


async def process_and_deliver_msg(context: ElroyContext, user_input: str, role=USER):
    if user_input.startswith("/") and role == USER:
        cmd = user_input[1:].split()[0]

        if cmd.lower() not in {f.__name__ for f in SYSTEM_COMMANDS}:
            context.io.sys_message(f"Unknown command: {cmd}")
        else:
            try:
                result = await invoke_system_command(context, user_input)
                context.io.sys_message(result)
            except Exception as e:
                context.io.sys_message(f"Error invoking system command: {e}")
    else:
        context.io.assistant_msg(process_message(context, user_input, role))


def print_memory_panel(context: ElroyContext, context_messages: Iterable[ContextMessage]) -> None:
    pipe(
        context_messages,
        filter(lambda m: not m.created_at or m.created_at > get_utc_now() - context.config.max_in_context_message_age),
        map(lambda m: m.memory_metadata),
        filter(lambda m: m is not None),
        concat,
        map(lambda m: f"{m.memory_type}: {m.name}"),
        unique,
        list,
        sorted,
        context.io.print_memory_panel,
    )
