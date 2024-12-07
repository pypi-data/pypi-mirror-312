from pydantic import AliasChoices, AwareDatetime, BaseModel, ConfigDict, Field

from snap_python.schemas.common import (
    BaseErrorResult,
    BaseResponse,
    Media,
    SnapApp,
    SnapBaseVersion,
    SnapConfinement,
)


class Snap(BaseModel):
    model_config = ConfigDict(extra="allow")
    apps: list[SnapApp] = Field(default_factory=list)
    base: SnapBaseVersion | None = None
    channel: str
    confinement: SnapConfinement
    contact: str
    description: str
    developer: str
    devmode: bool
    icon: str | None = None
    id: str
    ignore_validation: bool = Field(
        validation_alias=AliasChoices("ignore-validation", "ignore_validation"),
        serialization_alias="ignore-validation",
    )
    install_date: AwareDatetime = Field(
        validation_alias=AliasChoices("install-date", "install_date"),
        serialization_alias="install-date",
    )
    installed_size: int = Field(
        validation_alias=AliasChoices("installed-size", "installed_size"),
        serialization_alias="installed-size",
    )
    jailmode: bool
    license: str = "unset"
    links: dict[str, list[str]] | None = None
    media: list[Media] = Field(default_factory=list)
    mounted_from: str = Field(
        validation_alias=AliasChoices("mounted-from", "mounted_from"),
        serialization_alias="mounted-from",
    )
    name: str
    private: bool
    publisher: dict[str, str] | None = None
    revision: str
    status: str
    summary: str
    title: str | None = None
    tracking_channel: str | None = Field(
        validation_alias=AliasChoices("tracking-channel", "tracking_channel"),
        serialization_alias="tracking-channel",
        default=None,
    )
    type: str
    version: str
    website: str | None = None


class SingleSnapResponse(BaseResponse):
    result: Snap | BaseErrorResult


class SnapListResponse(BaseResponse):
    result: list[Snap]

    def __len__(self):
        return len(self.result)
