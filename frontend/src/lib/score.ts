import type { Promessa, StatusPromessa, Votacao } from "./types";

/**
 * Score de Coerência — versão 0.1.
 *
 * A metodologia é pública e auditável (ver a rota /metodologia). Qualquer
 * mudança nesta fórmula deve ser documentada e versionada neste repositório.
 *
 * Cálculo: 70% vem das promessas de campanha e 30% das votações nominais.
 * Se uma das fontes estiver vazia, a outra assume peso total.
 */
export const PESO_PROMESSAS = 0.7;
export const PESO_VOTOS = 0.3;

/** Pontos atribuídos a cada situação de promessa, de 0 a 1. */
export const PONTOS_POR_STATUS: Record<StatusPromessa, number> = {
  cumprida: 1,
  em_andamento: 0.5,
  sem_acao: 0.25,
  contraditada: 0,
};

export function calcularScore(promessas: Promessa[], votacoes: Votacao[]): number {
  const mediaPromessas =
    promessas.length > 0
      ? promessas.reduce((soma, p) => soma + PONTOS_POR_STATUS[p.status], 0) /
        promessas.length
      : null;

  const mediaVotos =
    votacoes.length > 0
      ? votacoes.filter((v) => v.coerenteComDiscurso).length / votacoes.length
      : null;

  if (mediaPromessas === null && mediaVotos === null) return 0;

  const pesoPromessas = mediaPromessas === null ? 0 : mediaVotos === null ? 1 : PESO_PROMESSAS;
  const pesoVotos = mediaVotos === null ? 0 : mediaPromessas === null ? 1 : PESO_VOTOS;

  return Math.round(
    (pesoPromessas * (mediaPromessas ?? 0) + pesoVotos * (mediaVotos ?? 0)) * 100,
  );
}

export interface FaixaScore {
  rotulo: string;
  /** Classes Tailwind para texto, fundo de badge e barra de progresso. */
  texto: string;
  fundo: string;
  barra: string;
}

export interface FaixaPercentual {
  rotulo: string;
  texto: string;
  fundo: string;
  barra: string;
}

/** Faixas visuais do percentual exibido: vermelho, laranja, azul e verde. */
export function faixaDePercentual(percentual: number): FaixaPercentual {
  if (percentual <= 25) {
    return {
      rotulo: "Entrega baixa",
      texto: "text-danger-700",
      fundo: "bg-danger-100",
      barra: "bg-danger-600",
    };
  }
  if (percentual <= 50) {
    return {
      rotulo: "Entrega parcial",
      texto: "text-warning-700",
      fundo: "bg-warning-100",
      barra: "bg-warning-600",
    };
  }
  if (percentual <= 80) {
    return {
      rotulo: "Boa entrega",
      texto: "text-primary-700",
      fundo: "bg-primary-100",
      barra: "bg-primary-600",
    };
  }
  return {
    rotulo: "Alta entrega",
    texto: "text-success-700",
    fundo: "bg-success-100",
    barra: "bg-success-600",
  };
}

/** Faixas de cor do score: >= 80 verde, 60–79 amarelo, < 60 vermelho. */
export function faixaDoScore(score: number): FaixaScore {
  if (score >= 80) {
    return {
      rotulo: "Alta coerência",
      texto: "text-success-700",
      fundo: "bg-success-100",
      barra: "bg-success-600",
    };
  }
  if (score >= 60) {
    return {
      rotulo: "Coerência média",
      texto: "text-warning-700",
      fundo: "bg-warning-100",
      barra: "bg-warning-600",
    };
  }
  return {
    rotulo: "Baixa coerência",
    texto: "text-danger-700",
    fundo: "bg-danger-100",
    barra: "bg-danger-600",
  };
}

/** Contagem de promessas por status, usada no perfil e no comparador. */
export function resumoPromessas(promessas: Promessa[]): Record<StatusPromessa, number> {
  const resumo: Record<StatusPromessa, number> = {
    cumprida: 0,
    em_andamento: 0,
    contraditada: 0,
    sem_acao: 0,
  };
  for (const p of promessas) resumo[p.status] += 1;
  return resumo;
}

/** Percentual de promessas com status cumprida, usado na cor das iniciais. */
export function percentualEntrega(promessas: Promessa[]): number {
  if (promessas.length === 0) return 0;
  return Math.round(
    (promessas.filter((promessa) => promessa.status === "cumprida").length / promessas.length) * 100,
  );
}

/** Percentual (0–100) de votos coerentes com o discurso de campanha. */
export function percentualVotosCoerentes(votacoes: Votacao[]): number {
  if (votacoes.length === 0) return 0;
  return Math.round(
    (votacoes.filter((v) => v.coerenteComDiscurso).length / votacoes.length) * 100,
  );
}
