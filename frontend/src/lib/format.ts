import type { Casa, StatusPromessa } from "./types";

/** Formata um valor em reais sem casas decimais (ex.: "R$ 326.400"). */
export function formatarMoeda(valor: number): string {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  });
}

/**
 * Converte ISO AAAA-MM-DD para DD/MM/AAAA sem usar objeto Date,
 * evitando divergências de fuso horário entre servidor e cliente.
 */
export function formatarData(iso: string): string {
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

export function rotuloCasa(casa: Casa): string {
  return casa === "camara" ? "Deputado(a) Federal" : "Senador(a) da República";
}

export const ROTULOS_STATUS: Record<StatusPromessa, string> = {
  cumprida: "Cumprida",
  em_andamento: "Em andamento",
  contraditada: "Contraditada",
  sem_acao: "Sem ação identificada",
};
