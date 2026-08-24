export type Casa = "camara" | "senado";

export type StatusPromessa =
  | "cumprida"
  | "em_andamento"
  | "contraditada"
  | "sem_acao";

export type TipoProposicao = "PL" | "PEC" | "REQ";

export type Tema =
  | "Saúde"
  | "Educação"
  | "Meio Ambiente"
  | "Economia"
  | "Segurança"
  | "Infraestrutura"
  | "Direitos Humanos"
  | "Transparência";

export type VotoNominal = "Sim" | "Não" | "Abstenção" | "Ausente";

export type StatusProposicao =
  | "Em tramitação"
  | "Aprovada"
  | "Sancionada"
  | "Arquivada";

export interface Promessa {
  id: string;
  texto: string;
  tema: Tema;
  fonteUrl: string;
  fonteDescricao: string;
  /** Data da declaração, em ISO AAAA-MM-DD. */
  data: string;
  /** Eleição de referência (ex.: "2022"). */
  eleicao: string;
  status: StatusPromessa;
  /** Descrição da ação legislativa vinculada (proposição ou votação), quando houver. */
  acaoRelacionada?: string;
}

/** Promessa enviada pela comunidade, ainda aguardando validação (moderação). */
export interface PromessaPendente extends Promessa {
  parlamentarId: string;
  validacoes: number;
  questionamentos: number;
  enviadaPor: string;
}

export interface Proposicao {
  id: string;
  tipo: TipoProposicao;
  /** Número oficial (ex.: "1452/2023"). */
  numero: string;
  ementa: string;
  tema: Tema;
  status: StatusProposicao;
  /** Data de apresentação, em ISO AAAA-MM-DD. */
  data: string;
}

export interface Votacao {
  id: string;
  materia: string;
  tema: Tema;
  /** Data da votação, em ISO AAAA-MM-DD. */
  data: string;
  voto: VotoNominal;
  coerenteComDiscurso: boolean;
}

export interface GastoCategoria {
  categoria: string;
  /** Valor total no ano, em R$. */
  valor: number;
}

export interface Parlamentar {
  /** Slug usado na URL (ex.: "ana-beatriz-ramos"). */
  id: string;
  nome: string;
  casa: Casa;
  partido: string;
  uf: string;
  mandato: string;
  /** Popularidade na plataforma (mock do ranking "mais acessados"). */
  acessos: number;
  promessas: Promessa[];
  proposicoes: Proposicao[];
  votacoes: Votacao[];
  gastos: GastoCategoria[];
}
