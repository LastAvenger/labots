# -*- encoding: UTF-8 -*-
import logging
from typing import List, Dict, Any
from sqlitedict import SqliteDict

from ..common.message import Message
from ..common.event import Event
from ..common.action import Action
from ..utils import override
from ..storage import Storage
from ..cache import Cache

# Initialize logging
logger = logging.getLogger(__name__)

class Bot(Event):
    _name = None

    targets: List[Any] = {} # TODO: str or dict?
    config: Dict = {}
    allow_reload: bool = True
    logger: logging.Logger = None
    action: Action = None
    storage: SqliteDict = None
    cache: SqliteDict = None

    @override.non_overridable
    def __init__(self,
            name: str = '<unknown>',
            action: Action = None,
            config: Dict = {},
            storage: Storage = None,
            cache: Cache = None):
        self._name = name
        self.logger = logging.getLogger(__name__ + ':' + name)
        self.action = action
        self.config = config
        self.storage = storage.open('bots.' + name)
        self.cache = cache.open('bots.' + name)

    @override.non_overridable
    def __del__(self):
        self.storage.close()
        self.cache.close()

    """
    Bot phase callbacks
    """

    @override.non_overridden
    def init(self):
        pass

    @override.non_overridden
    def finalize(self):
        pass

    """
    Implement ..common.event.Event
    """

    @override.non_overridden
    def on_raw(self, msg: Message):
        pass

    @override.non_overridden
    def on_connect(self):
        pass

    @override.non_overridden
    def on_message(self, origin: str, target: str, msg: str):
        pass

    @override.non_overridden
    def on_channel_message(self, origin: str, channel: str, msg: str):
        pass

    """
    Utils functions
    """
    @override.non_overridable
    def is_in_targets(self, target: str) -> bool:
        for t in self.targets:
            if isinstance(t, str):
                if self.action.is_same_target(target, t):
                    return True
            elif isinstance(t, dict) and 'targets' in t:
                if self.action.is_same_target(target, t['target']):
                    return True
        return False
