import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { parlamentares } from "@/data/mock";
import { calcularScore, percentualVotosCoerentes, resumoPromessas } from "@/lib/score";
import { formatarData, formatarMoeda, rotuloCasa } from "@/lib/format";
import Avatar from "@/components/Avatar";
import GastosChart from "@/components/GastosChart";
import PerfilTabs from "@/components/PerfilTabs";
import ScoreBadge from "@/components/ScoreBadge";
import StatusPromessaBadge from "@/components/StatusPromessaBadge";
import TabelaProposicoes from "@/components/TabelaProposicoes";

interface PerfilPageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return parlamentares.map(({ id }) => ({ id }));
}

export async function generateMetadata({ params }: PerfilPageProps): Promise<Metadata> {
  const { id } = await params;
  const parlamentar = parlamentares.find((item) => item.id === id);
  return { title: parlamentar?.nome ?? "Parlamentar" };
}

export default async function PerfilParlamentar({ params }: PerfilPageProps) {
  const { id } = await params;
  const parlamentar = parlamentares.find((item) => item.id === id);
  if (!parlamentar) notFound();

  const score = calcularScore(parlamentar.promessas, parlamentar.votacoes);
  const resumo = resumoPromessas(parlamentar.promessas);

  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <section className="rounded-2xl border border-primary-200 bg-primary-50 p-6 sm:p-8">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <Avatar nome={parlamentar.nome} tamanho="lg" percentual={score} />
            <div>
              <p className="text-sm font-semibold text-primary-700">{rotuloCasa(parlamentar.casa)}</p>
              <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-neutral-900">{parlamentar.nome}</h1>
              <p className="mt-1 text-neutral-700">{parlamentar.partido}/{parlamentar.uf} · mandato {parlamentar.mandato}</p>
            </div>
          </div>
          <ScoreBadge score={score} grande />
        </div>
      </section>

      <section className="mt-5 flex flex-col gap-4 rounded-xl border border-success-200 bg-success-50 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="font-bold text-success-900">Encontrou uma promessa deste parlamentar?</h2>
          <p className="mt-1 text-sm text-success-800">Registre a declaração original e ajude a manter este perfil verificável.</p>
        </div>
        <Link href={`/promessas/nova?parlamentar=${parlamentar.id}`} className="inline-flex min-h-11 shrink-0 items-center justify-center rounded-lg bg-success-700 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-success-600">Cadastrar promessa</Link>
      </section>

      <section className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {[
          ["Promessas", parlamentar.promessas.length],
          ["Cumpridas", resumo.cumprida],
          ["Proposições", parlamentar.proposicoes.length],
          ["Votos coerentes", `${percentualVotosCoerentes(parlamentar.votacoes)}%`],
        ].map(([rotulo, valor]) => (
          <div key={rotulo} className="rounded-xl border border-neutral-200 bg-white p-4 shadow-sm">
            <p className="font-data text-2xl font-extrabold text-neutral-900">{valor}</p>
            <p className="mt-1 text-sm text-neutral-600">{rotulo}</p>
          </div>
        ))}
      </section>

      <div className="mt-10">
        <PerfilTabs
          abas={[
            { id: "promessas", rotulo: "Promessas", conteudo: <Promessas parlamentar={parlamentar} /> },
            { id: "proposicoes", rotulo: "Proposições", conteudo: <TabelaProposicoes proposicoes={parlamentar.proposicoes} /> },
            { id: "votacoes", rotulo: "Votações", conteudo: <Votacoes parlamentar={parlamentar} /> },
            { id: "gastos", rotulo: "Gastos", conteudo: <Gastos parlamentar={parlamentar} /> },
          ]}
        />
      </div>
      <p className="mt-8 text-xs text-neutral-500">Perfil demonstrativo. Dados fictícios, sem persistência.</p>
    </div>
  );
}

function Promessas({ parlamentar }: { parlamentar: (typeof parlamentares)[number] }) {
  return (
    <div className="space-y-4">
      {parlamentar.promessas.map((promessa) => (
        <article key={promessa.id} className={`rounded-xl border border-neutral-200 border-l-4 bg-white p-5 shadow-sm ${promessa.status === "cumprida" ? "border-l-success-500" : promessa.status === "em_andamento" ? "border-l-warning-500" : promessa.status === "contraditada" ? "border-l-danger-500" : "border-l-neutral-400"}`}>
          <div className="flex flex-wrap items-start justify-between gap-3">
            <h2 className="max-w-3xl font-semibold leading-6 text-neutral-900">{promessa.texto}</h2>
            <StatusPromessaBadge status={promessa.status} />
          </div>
          <p className="mt-3 text-sm text-neutral-600">{promessa.tema} · declaração em {formatarData(promessa.data)} · eleição {promessa.eleicao}</p>
          <a href={promessa.fonteUrl} target="_blank" rel="noreferrer" className="mt-2 block text-sm text-primary-700 hover:underline">Fonte: {promessa.fonteDescricao}</a>
          {promessa.acaoRelacionada && <p className="mt-3 border-t border-neutral-200 pt-3 text-sm text-neutral-700"><strong>Ação relacionada:</strong> {promessa.acaoRelacionada}</p>}
        </article>
      ))}
    </div>
  );
}

function Votacoes({ parlamentar }: { parlamentar: (typeof parlamentares)[number] }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-neutral-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-neutral-200 bg-neutral-100 text-xs uppercase tracking-wider text-neutral-600"><tr><th className="px-4 py-3">Matéria</th><th className="px-4 py-3">Voto</th><th className="px-4 py-3">Data</th><th className="px-4 py-3">Coerência</th></tr></thead>
        <tbody className="divide-y divide-neutral-200">{parlamentar.votacoes.map((votacao) => <tr key={votacao.id}><td className="px-4 py-4 font-medium text-neutral-900">{votacao.materia}<span className="block text-xs font-normal text-neutral-500">{votacao.tema}</span></td><td className="px-4 py-4 text-neutral-800">{votacao.voto}</td><td className="px-4 py-4 text-neutral-600">{formatarData(votacao.data)}</td><td className={`px-4 py-4 font-semibold ${votacao.coerenteComDiscurso ? "text-success-700" : "text-danger-700"}`}>{votacao.coerenteComDiscurso ? "Coerente" : "Divergente"}</td></tr>)}</tbody>
      </table>
    </div>
  );
}

function Gastos({ parlamentar }: { parlamentar: (typeof parlamentares)[number] }) {
  return <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_280px]"><div className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"><h2 className="text-xl font-bold text-neutral-900">Distribuição dos gastos</h2><div className="mt-5"><GastosChart gastos={parlamentar.gastos} /></div></div><aside className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"><p className="text-sm text-neutral-600">Total anual</p><p className="mt-1 font-data text-3xl font-extrabold text-primary-700">{formatarMoeda(parlamentar.gastos.reduce((total, item) => total + item.valor, 0))}</p><p className="mt-3 text-sm text-neutral-600">Valores de demonstração organizados por categoria.</p></aside></div>;
}
