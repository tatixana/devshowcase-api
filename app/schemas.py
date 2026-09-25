from pydantic import BaseModel, ConfigDict, HttpUrl, TypeAdapter, ValidationError, field_validator

# ---------- Funções de validação reutilizadas pelos schemas ----------

http_url = TypeAdapter(HttpUrl)


def validar_texto_obrigatorio(valor: str) -> str:
    """Remove espaços das pontas e não aceita texto vazio."""
    valor = valor.strip()
    if valor == "":
        raise ValueError("Este campo é obrigatório e não pode ficar vazio.")
    return valor


def validar_url(valor: str | None) -> str | None:
    """Aceita URL vazia (campo opcional), mas se for informada precisa ser válida."""
    if valor is None or valor.strip() == "":
        return None
    valor = valor.strip()
    try:
        http_url.validate_python(valor)
    except ValidationError:
        raise ValueError("URL inválida. Use um endereço completo, como https://github.com/usuario")
    return valor


# ---------- PROFILE ----------

class ProfileCreate(BaseModel):
    """Dados de ENTRADA para cadastrar um perfil."""
    name: str
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None

    @field_validator("name")
    @classmethod
    def checar_nome(cls, valor):
        return validar_texto_obrigatorio(valor)

    @field_validator("github_url", "linkedin_url")
    @classmethod
    def checar_urls(cls, valor):
        return validar_url(valor)


class ProfileResponse(BaseModel):
    """Dados de SAÍDA de um perfil."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str | None
    github_url: str | None
    linkedin_url: str | None


# ---------- TECHNOLOGY ----------

class TechnologyCreate(BaseModel):
    """Dados de ENTRADA para cadastrar uma tecnologia."""
    name: str

    @field_validator("name")
    @classmethod
    def checar_nome(cls, valor):
        return validar_texto_obrigatorio(valor)


class TechnologyResponse(BaseModel):
    """Dados de SAÍDA de uma tecnologia."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# ---------- PROJECT ----------

class ProjectCreate(BaseModel):
    """Dados de ENTRADA para cadastrar um projeto."""
    title: str
    description: str | None = None
    repository_url: str | None = None
    demo_url: str | None = None
    profile_id: int
    technology_ids: list[int] = []

    @field_validator("title")
    @classmethod
    def checar_titulo(cls, valor):
        return validar_texto_obrigatorio(valor)

    @field_validator("repository_url", "demo_url")
    @classmethod
    def checar_urls(cls, valor):
        return validar_url(valor)


class ProjectResponse(BaseModel):
    """Dados de SAÍDA de um projeto, já com o perfil e as tecnologias relacionadas."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    repository_url: str | None
    demo_url: str | None
    profile_id: int
    profile: ProfileResponse
    technologies: list[TechnologyResponse]
