import type { Metadata } from "next";
import Link from "next/link";
import { parlamentares } from "@/data/mock";
import type { Casa } from "@/lib/types";
import ParlamentarCard from "@/components/ParlamentarCard";

export const metadata: Metadata = {
  title: "Parlamentares",
  description: "Busque e filtre deputados federais e senadores monitorados.",
};

function primeiroParametro(valor: string | string[] | undefined): string {
  return Array.isArray(valor) ? (valor[0] ?? "") : (valor ?? "");
}

export default async function Parlamentares({
  searchParams,
}: PageProps<"/parlamentares">) {
  const parametros = await searchParams;
  const q = primeiroParametro(parametros.q);
  const casa = primeiroParametro(parametros.casa);
  const uf = primeiroParametro(parametros.uf);
  const partido = primeiroParametro(parametros.partido);

  const ufs = [...new Set(parlamentares.map((p) => p.uf))].sort();
  const partidos = [...new Set(parlamentares.map((p) => p.partido))].sort();

  const termo = q.trim().toLowerCase();
  const filtrados = parlamentares.filter((p) => {
    if (casa && p.casa !== (casa as Casa)) return false;
    if (uf && p.uf !== uf) return false;
    if (partido && p.partido !== partido) return false;
    if (
      termo &&
      !`${p.nome} ${p.partido} ${p.uf}`.toLowerCase().includes(termo)
    )
      return false;
    return true;
  });

  const select =
    "min-h-11 rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm";

  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Dados públicos em foco</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Parlamentares</h1>
      <p className="mt-2 text-neutral-600">
        Busque por nome, partido ou UF, ou filtre por casa legislativa.
      </p>

      <form
        action="/parlamentares"
        className="mt-8 flex flex-wrap items-center gap-3 rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"
      >
        <input
          type="search"
          name="q"
          defaultValue={q}
          placeholder="Buscar por nome…"
          className="min-h-11 min-w-48 flex-1 rounded-md border border-neutral-300 px-3 py-2 text-sm"
        />
        <select name="casa" defaultValue={casa} className={select}>
          <option value="">Todas as casas</option>
          <option value="camara">Câmara dos Deputados</option>
          <option value="senado">Senado Federal</option>
        </select>
        <select name="uf" defaultValue={uf} className={select}>
          <option value="">Todos os estados</option>
          {ufs.map((sigla) => (
            <option key={sigla} value={sigla}>
              {sigla}
            </option>
          ))}
        </select>
        <select name="partido" defaultValue={partido} className={select}>
          <option value="">Todos os partidos</option>
          {partidos.map((sigla) => (
            <option key={sigla} value={sigla}>
              {sigla}
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="min-h-11 rounded-md bg-primary-700 px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-600 active:bg-primary-800"
        >
          Filtrar
        </button>
      </form>

      <p className="mt-6 text-sm text-neutral-600">
        {filtrados.length}{" "}
        {filtrados.length === 1 ? "parlamentar encontrado" : "parlamentares encontrados"}
      </p>
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {filtrados.map((p) => (
          <ParlamentarCard key={p.id} parlamentar={p} />
        ))}
      </div>
      {filtrados.length === 0 && (
        <p className="mt-8 rounded-xl border border-dashed border-neutral-300 bg-white p-8 text-center text-neutral-500">
          Nenhum parlamentar encontrado com esses filtros.{" "}
          <Link href="/parlamentares" className="text-primary-700 hover:underline">
            Limpar filtros
          </Link>
        </p>
      )}
    </div>
  );
}
