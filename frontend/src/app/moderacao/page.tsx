import type { Metadata } from "next";
import Link from "next/link";
import { promessasPendentes, parlamentares } from "@/data/mock";
import { formatarData } from "@/lib/format";
import BotoesValidacao from "@/components/BotoesValidacao";
import StatusPromessaBadge from "@/components/StatusPromessaBadge";

export const metadata: Metadata = {
  title: "Fila de moderação",
  description: "Revise e valide promessas enviadas pela comunidade.",
};

export default function Moderacao() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Participação cidadã</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Fila de moderação</h1>
      <p className="mt-2 max-w-2xl text-neutral-600">Confira a fonte, valide o registro ou questione informações que precisem de revisão.</p>
      <div className="mt-8 space-y-4">
        {promessasPendentes.map((promessa) => {
          const parlamentar = parlamentares.find((p) => p.id === promessa.parlamentarId);
          return (
            <article key={promessa.id} className="rounded-xl border border-neutral-200 border-l-4 border-l-warning-500 bg-white p-5 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-primary-700">{parlamentar?.nome ?? "Parlamentar não encontrado"}</p>
                  <h2 className="mt-2 text-lg font-bold text-neutral-900">{promessa.texto}</h2>
                </div>
                <StatusPromessaBadge status={promessa.status} />
              </div>
              <p className="mt-4 text-sm text-neutral-600">{promessa.fonteDescricao} · declaração em {formatarData(promessa.data)}</p>
              <a href={promessa.fonteUrl} target="_blank" rel="noreferrer" className="mt-1 block truncate text-sm text-primary-700 hover:underline">Conferir fonte: {promessa.fonteUrl}</a>
              <div className="mt-5 flex flex-wrap items-center justify-between gap-4 border-t border-neutral-200 pt-4">
                <p className="text-xs text-neutral-600">{promessa.validacoes} validações · {promessa.questionamentos} questionamentos · enviada por {promessa.enviadaPor}</p>
                <BotoesValidacao />
              </div>
            </article>
          );
        })}
      </div>
      <p className="mt-8 text-sm text-neutral-600">Quer contribuir com um novo registro? <Link href="/promessas/nova" className="font-semibold text-primary-700 hover:underline">Cadastre uma promessa</Link>.</p>
    </div>
  );
}
