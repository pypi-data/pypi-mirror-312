import json
import logging

from ceo import Agent

log = logging.getLogger('ceo.ability')


def agentic(agent: Agent):
    def decorator(func):
        def wrapper(query: str, *args, **kwargs) -> str:
            return agent.assign(query).just_do_it()
        wrapper.__name__ = f'talk_to_{agent.name}'
        wrapper.__doc__ = json.dumps({
            "description": {
                "brief_description": f'Initiates a conversation with "{agent.name}" to use its abilities.',
                "detailed_description": f"First, carefully consider and explore {agent.name}'s potential abilities in solving your tasks, "
                                        f"then, if you need {agent.name}'s help, you must tell comprehensively, precisely "
                                        f"and exactly what you need {agent.name} to do.",
                f"self_introduction_from_{agent.name}": agent.introduction,
                f"metadata_of_{agent.name}": agent.__repr__(),
                "args": [{
                    "query": {
                      "name": "query",
                      "type": "str",
                      "description": f"a comprehensively, precisely and exactly instruction to be processed by {agent.name}."
                    }
                  }
                ],
                "returns": {
                  "type": "str",
                  "description": f"{agent.name}'s response to your instruction."
                }
            }
        }, ensure_ascii=False)
        log.debug(f'Agent dispatcher generated. {wrapper.__name__}: {wrapper.__doc__}')
        return wrapper
    return decorator
