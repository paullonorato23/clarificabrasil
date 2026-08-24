import type { Metadata } from "next";
import { parlamentares } from "@/data/mock";
import ComparadorClient from "@/components/ComparadorClient";

export const metadata: Metadata = {
  title: "Comparar parlamentares",
  description: "Compare indicadores públicos de dois parlamentares lado a lado.",
};

function primeiroParametro(valor: string | string[] | undefined): string {
  return Array.isArray(valor) ? (valor[0] ?? "") : (valor ?? "");
}

export default async function Comparar({ searchParams }: PageProps<"/comparar">) {
  const parametros = await searchParams;
  const a = primeiroParametro(parametros.a);
  const b = primeiroParametro(parametros.b);

  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Leitura lado a lado</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Comparar parlamentares</h1>
      <p className="mt-2 max-w-2xl text-neutral-600">
        Escolha dois perfis para comparar promessas, proposições, votos e gastos de gabinete.
      </p>
      <div className="mt-8"><ComparadorClient parlamentares={parlamentares} inicialA={a} inicialB={b} /></div>
    </div>
  );
}
