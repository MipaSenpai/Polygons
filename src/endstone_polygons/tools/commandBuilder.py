from typing_extensions import Self
from typing import Any, Literal, Optional, Union


PermissionDefault = Union[
    bool,
    Literal["true", "false", "op", "not_op", "console"]
]


class Permission:
    def __init__(
        self,
        name: str,
        description: str,
        default: PermissionDefault = "op"
    ) -> None:
        self.__name: str = name
        self.__description: str = description
        self.__default: PermissionDefault = default
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def default(self) -> PermissionDefault:
        return self.__default
    
    def toDict(self) -> dict[str, Any]:
        return {
            "description": self.__description,
            "default": self.__default
        }


class Command:
    def __init__(
        self,
        name: str,
        description: str,
        usages: Optional[Union[list[str], str]] = None,
        permissions: Optional[Union[list[Union[str, Permission]], str, Permission]] = None,
        aliases: Optional[Union[list[str], str]] = None
    ) -> None:
        self.__name: str = name
        self.__description: str = description
        
        if usages is None:
            self.__usages: list[str] = [f"/{name}"]
        elif isinstance(usages, str):
            self.__usages = [usages]
        else:
            self.__usages = usages
        
        if permissions is None:
            self.__permissions: list[Union[str, Permission]] = []
        elif isinstance(permissions, (str, Permission)):
            self.__permissions = [permissions]
        else:
            self.__permissions = permissions
        
        if aliases is None:
            self.__aliases: Optional[list[str]] = None
        elif isinstance(aliases, str):
            self.__aliases = [aliases]
        else:
            self.__aliases = aliases
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def usages(self) -> list[str]:
        return self.__usages
    
    @property
    def aliases(self) -> Optional[list[str]]:
        return self.__aliases
    
    def toDict(self) -> dict[str, Any]:
        cmdDict: dict[str, Any] = {
            "description": self.__description,
            "usages": self.__usages,
        }
        
        if self.__permissions:
            permission_names: list[str] = []
            for perm in self.__permissions:
                if isinstance(perm, Permission):
                    permission_names.append(perm.name)
                else:
                    permission_names.append(perm)
            cmdDict["permissions"] = permission_names
        
        if self.__aliases:
            cmdDict["aliases"] = self.__aliases
        
        return cmdDict
    
    def getPermissions(self) -> dict[str, dict[str, Any]]:
        perms: dict[str, dict[str, Any]] = {}
        for perm in self.__permissions:
            if isinstance(perm, Permission):
                perms[perm.name] = perm.toDict()
        return perms


class CommandBuilder:
    def __init__(self) -> None:
        self.__commands: dict[str, dict[str, Any]] = {}
        self.__permissions: dict[str, dict[str, Any]] = {}
    
    def add(self, command: Command) -> Self:
        self.__commands[command.name] = command.toDict()
        self.__permissions.update(command.getPermissions())
        return self
    
    @property
    def commands(self) -> dict[str, dict[str, Any]]:
        return self.__commands
    
    @property
    def permissions(self) -> dict[str, dict[str, Any]]:
        return self.__permissions