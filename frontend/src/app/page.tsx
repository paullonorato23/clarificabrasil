import Link from "next/link";
import { parlamentares, promessasPendentes } from "@/data/mock";
import { calcularScore } from "@/lib/score";
import ParlamentarCard from "@/components/ParlamentarCard";

export default function Inicio() {
  const totalPromessas = parlamentares.reduce((s, p) => s + p.promessas.length, 0);
  const totalProposicoes = parlamentares.reduce((s, p) => s + p.proposicoes.length, 0);
  const totalVotacoes = parlamentares.reduce((s, p) => s + p.votacoes.length, 0);

  const porScore = [...parlamentares].sort(
    (a, b) =>
      calcularScore(b.promessas, b.votacoes) - calcularScore(a.promessas, a.votacoes),
  );
  const maisAcessados = [...parlamentares].sort((a, b) => b.acessos - a.acessos);

  return (
    <div>
      {/* Hero com busca */}
      <section className="bg-primary-900 text-white">
        <div className="mx-auto max-w-6xl px-4 py-14 text-center sm:py-20">
          <h1 className="text-3xl font-extrabold sm:text-4xl">
            O que seu representante <span className="text-primary-300">prometeu</span>
            <br className="hidden sm:block" /> vs. o que ele{" "}
            <span className="text-primary-300">realmente fez</span>?
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-primary-100">
            Cruzamos promessas de campanha com proposições, votações e gastos de
            deputados e senadores — com dados oficiais e código aberto.
          </p>
          <form action="/parlamentares" className="mx-auto mt-8 flex max-w-xl flex-col gap-3 sm:flex-row">
            <input
              type="search"
              name="q"
              placeholder="Busque por nome, partido ou UF…"
              className="min-h-12 flex-1 rounded-lg border border-white/20 px-4 py-3 text-neutral-900 placeholder:text-neutral-500"
            />
            <button
              type="submit"
              className="min-h-12 rounded-lg bg-success-500 px-5 py-3 font-semibold text-success-900 hover:bg-success-400"
            >
              Buscar
            </button>
          </form>
        </div>
      </section>

      {/* Estatísticas gerais */}
      <section className="border-b border-neutral-200 bg-white">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-4 px-4 py-8 text-center sm:grid-cols-4">
          {[
            { valor: parlamentares.length, rotulo: "Parlamentares monitorados" },
            { valor: totalPromessas, rotulo: "Promessas cadastradas" },
            { valor: totalProposicoes, rotulo: "Proposições acompanhadas" },
            { valor: totalVotacoes, rotulo: "Votações analisadas" },
          ].map((item) => (
            <div key={item.rotulo}>
              <p className="font-data text-3xl font-extrabold text-primary-700">{item.valor}</p>
              <p className="mt-1 text-sm text-neutral-600">{item.rotulo}</p>
            </div>
          ))}
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-4">
        <section className="mt-8 flex flex-col gap-5 rounded-2xl bg-primary-700 p-6 text-white shadow-lg sm:flex-row sm:items-center sm:justify-between sm:p-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-primary-200">Ajude a tornar o monitoramento completo</p>
            <h2 className="mt-2 text-2xl font-extrabold">Você viu uma promessa? Cadastre a fonte.</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-primary-100">A comunidade ajuda a registrar declarações verificáveis para que o acompanhamento seja mais completo.</p>
          </div>
          <Link href="/promessas/nova" className="inline-flex min-h-12 shrink-0 items-center justify-center rounded-lg bg-white px-5 py-3 text-sm font-bold text-primary-800 shadow-sm hover:bg-primary-50">Cadastrar promessa</Link>
        </section>

        {/* Rankings */}
        <div className="mt-10 grid gap-8 lg:grid-cols-2">
          <section>
            <div className="mb-4 flex items-baseline justify-between">
              <h2 className="text-xl font-bold text-neutral-900">Maiores scores de coerência</h2>
              <Link href="/metodologia" className="text-sm text-primary-700 hover:underline">
                Como calculamos?
              </Link>
            </div>
            <div className="space-y-3">
              {porScore.slice(0, 3).map((p) => (
                <ParlamentarCard key={p.id} parlamentar={p} />
              ))}
            </div>
          </section>
          <section>
            <h2 className="mb-4 text-xl font-bold text-neutral-900">Mais acessados</h2>
            <div className="space-y-3">
              {maisAcessados.slice(0, 3).map((p) => (
                <ParlamentarCard key={p.id} parlamentar={p} />
              ))}
            </div>
          </section>
        </div>

        {/* CTAs */}
        <section className="mt-12 grid gap-4 pb-4 sm:grid-cols-3">
          <Link
            href="/comparar"
            className="rounded-xl border border-neutral-200 bg-white p-6 transition hover:border-primary-300 hover:shadow-md"
          >
            <h3 className="font-bold text-neutral-900">⚖️ Comparar parlamentares</h3>
            <p className="mt-1 text-sm text-neutral-600">
              Compare lado a lado promessas, proposições, votos e gastos.
            </p>
          </Link>
          <Link
            href="/promessas/nova"
            className="rounded-xl border border-primary-300 bg-primary-50 p-6 shadow-md transition hover:border-primary-500 hover:shadow-lg"
          >
            <h3 className="font-bold text-primary-900">📋 Cadastrar promessa</h3>
            <p className="mt-1 text-sm text-neutral-700">
              O monitoramento é colaborativo: cadastre uma promessa com fonte verificável.
            </p>
          </Link>
          <Link
            href="/moderacao"
            className="rounded-xl border border-neutral-200 bg-white p-6 transition hover:border-primary-300 hover:shadow-md"
          >
            <h3 className="font-bold text-neutral-900">🔍 Fila de moderação</h3>
            <p className="mt-1 text-sm text-neutral-600">
              {promessasPendentes.length} promessas aguardando validação da comunidade.
            </p>
          </Link>
        </section>
      </div>
    </div>
  );
}
