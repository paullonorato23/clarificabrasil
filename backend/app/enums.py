"""Enums de domínio. Os valores são idênticos aos tipos do frontend
(`frontend/src/lib/types.ts`), pois trafegam como string no JSON da API."""

from enum import Enum


class Casa(str, Enum):
    CAMARA = "camara"
    SENADO = "senado"


class Tema(str, Enum):
    SAUDE = "Saúde"
    EDUCACAO = "Educação"
    MEIO_AMBIENTE = "Meio Ambiente"
    ECONOMIA = "Economia"
    SEGURANCA = "Segurança"
    INFRAESTRUTURA = "Infraestrutura"
    DIREITOS_HUMANOS = "Direitos Humanos"
    TRANSPARENCIA = "Transparência"


class StatusPromessa(str, Enum):
    CUMPRIDA = "cumprida"
    EM_ANDAMENTO = "em_andamento"
    CONTRADITADA = "contraditada"
    SEM_ACAO = "sem_acao"


class TipoProposicao(str, Enum):
    PL = "PL"
    PEC = "PEC"
    REQ = "REQ"


class StatusProposicao(str, Enum):
    EM_TRAMITACAO = "Em tramitação"
    APROVADA = "Aprovada"
    SANCIONADA = "Sancionada"
    ARQUIVADA = "Arquivada"


class VotoNominal(str, Enum):
    SIM = "Sim"
    NAO = "Não"
    ABSTENCAO = "Abstenção"
    AUSENTE = "Ausente"


class PapelUsuario(str, Enum):
    COMUM = "comum"
    MODERADOR = "moderador"


class SituacaoModeracao(str, Enum):
    PENDENTE = "pendente"
    PUBLICADA = "publicada"
    REJEITADA = "rejeitada"


class TipoValidacao(str, Enum):
    VALIDACAO = "validacao"
    QUESTIONAMENTO = "questionamento"
