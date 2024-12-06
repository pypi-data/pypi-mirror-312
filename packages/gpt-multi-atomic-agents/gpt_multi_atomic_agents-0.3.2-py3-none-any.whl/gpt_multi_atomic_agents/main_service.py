import logging
import typing

from atomic_agents.agents.base_agent import (
    BaseAgent,
    BaseAgentConfig,
)
from cornsnake import util_time, util_wait
from rich.console import Console

from . import main_router

from . import util_ai
from .agent_definition import (
    AgentDefinitionBase,
    FunctionAgentDefinition,
)
from .blackboard import (
    Blackboard,
    FunctionCallBlackboard,
    GraphQLBlackboard,
    Message,
    MessageRole,
)
from .config import Config
from .functions_dto import FunctionAgentOutputSchema
from . import util_print_agent

console = Console()

logger = logging.getLogger("main_service")


def _create_agent(agent_definition: AgentDefinitionBase, _config: Config) -> BaseAgent:
    client, model, max_tokens = util_ai.create_client(_config=_config)
    system_prompt_builder = agent_definition.get_system_prompt_builder(_config=_config)

    agent = BaseAgent(
        config=BaseAgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt_builder.build_system_prompt(),
            input_schema=agent_definition.input_schema,
            output_schema=agent_definition.output_schema,
            max_tokens=max_tokens,
        )
    )
    return agent


def _check_blackboard(
    blackboard: Blackboard, agent_definitions: list[AgentDefinitionBase]
) -> None:
    is_function_based = isinstance(agent_definitions[0], FunctionAgentDefinition)
    if blackboard:
        if is_function_based and not (typing.cast(FunctionCallBlackboard, blackboard)):
            raise RuntimeError("Expected blackboard to be a FunctionCallBlackboard")


def _create_blackboard(agent_definitions: list[AgentDefinitionBase]) -> Blackboard:
    if not agent_definitions:
        raise RuntimeError("Expected at least 1 Agent Definition")
    is_function_based = isinstance(agent_definitions[0], FunctionAgentDefinition)
    blackboard = FunctionCallBlackboard() if is_function_based else GraphQLBlackboard()
    return blackboard


def generate(
    agent_definitions: list[AgentDefinitionBase],
    chat_agent_description: str,
    _config: Config,
    user_prompt: str,
    blackboard: Blackboard
    | None = None,  # If used as a web service, then would also accept previous state + new data (which the user has updated either by executing its implementation of Function Calls OR by updating via GraphQL mutations).
    execution_plan: main_router.AgentExecutionPlan | None = None,
) -> Blackboard:
    """
    Use the provided agents to fulfill the user's prompt.
    - if an execution plan is provided, that is used to decide which agents to execute.
       - else the router is used to generate an execution plan
    """

    start = util_time.start_timer()

    if blackboard:
        _check_blackboard(blackboard=blackboard, agent_definitions=agent_definitions)
    else:
        blackboard = _create_blackboard(agent_definitions)

    blackboard.previous_messages.append(
        Message(role=MessageRole.user, message=user_prompt)
    )

    with console.status("[bold green]Processing...") as _status:
        try:
            if not execution_plan:
                execution_plan = main_router.generate_plan(
                    agent_definitions=agent_definitions,
                    chat_agent_description=chat_agent_description,
                    _config=_config,
                    user_prompt=user_prompt,
                )
                blackboard.previous_messages.append(
                    Message(
                        role=MessageRole.assistant, message=execution_plan.chat_message
                    )
                )
                util_wait.wait_seconds(_config.delay_between_calls_in_seconds)

            # Loop thru all the recommended agents, sending each one a rewritten version of the user prompt
            for i, recommended_agent in enumerate(execution_plan.recommended_agents):
                try:
                    if recommended_agent.agent_name == "chat":
                        # TODO: add option to redirect to some Chat agent
                        continue

                    console.log(
                        f":robot: Executing agent {recommended_agent.agent_name}..."
                    )
                    util_print_agent.print_agent(
                        recommended_agent, _config=_config, prefix="EXECUTING: "
                    )
                    matching_agent_definitions = list(
                        filter(
                            lambda a: a.agent_name == recommended_agent.agent_name,
                            agent_definitions,
                        )
                    )
                    if not matching_agent_definitions:
                        raise RuntimeError(
                            f"Could not match recommended agent {recommended_agent.agent_name}"
                        )
                    if len(matching_agent_definitions) > 1:
                        console.print(
                            f":warning: Matched more than one agent to {recommended_agent.agent_name}"
                        )
                    agent_definition = matching_agent_definitions[0]
                    agent = _create_agent(agent_definition, _config=_config)

                    response = agent.run(
                        agent_definition.build_input(
                            recommended_agent.rewritten_user_prompt,
                            blackboard=blackboard,
                            config=_config,
                        )
                    )
                    util_print_agent.print_assistant_output(response, agent_definition)

                    agent_definition.update_blackboard(
                        response=response, blackboard=blackboard
                    )
                    is_last = i == len(execution_plan.recommended_agents) - 1
                    if not is_last:
                        util_wait.wait_seconds(_config.delay_between_calls_in_seconds)
                except Exception as e:
                    logger.exception(e)
        except Exception as e:
            logger.exception(e)

        console.log(":robot: (done)")
        time_taken = util_time.end_timer(start=start)
        console.log(f"  time taken: {util_time.describe_elapsed_seconds(time_taken)}")
    return blackboard


def run_chat_loop(
    agent_definitions: list[AgentDefinitionBase],
    chat_agent_description: str,
    _config: Config,
    given_user_prompt: str | None = None,
    blackboard: Blackboard
    | None = None,  # If used as a web service, then would also accept previous state + new data (which the user has updated either by executing its implementation of Function Calls OR by updating via GraphQL mutations).
) -> Blackboard:
    """
    Use the provided agents to fulfill the user's prompt.
    - if an execution plan is provided, that is used to decide which agents to execute.
       - else the router is used to generate an execution plan
    - if no given user prompt is provided, then the user is prompted via keyboard input in a REPL loop.
    """

    if not blackboard:
        blackboard = _create_blackboard(agent_definitions)

    initial_assistant_message = "How can I help you?"
    initial_message = FunctionAgentOutputSchema(
        chat_message=initial_assistant_message, generated_function_calls=[]
    )

    util_print_agent.print_assistant_functions(initial_message)

    blackboard.previous_messages.append(
        Message(role=MessageRole.assistant, message=initial_assistant_message)
    )

    # for more emojis - see "poetry run python -m rich.emoji"
    if given_user_prompt:
        util_print_agent.print_user_prompt(given_user_prompt)

    while True:
        user_prompt = (
            given_user_prompt
            if given_user_prompt
            else console.input(":sunglasses: You: ")
        )
        if not user_prompt:
            break

        blackboard = generate(
            agent_definitions=agent_definitions,
            chat_agent_description=chat_agent_description,
            _config=_config,
            user_prompt=user_prompt,
            blackboard=blackboard,
        )

        if given_user_prompt:
            break
    # To support a stateless web service, we return the whole blackboard, and accept it as optional input
    return blackboard


# to debug - see agent.system_prompt_generator.generate_prompt()
