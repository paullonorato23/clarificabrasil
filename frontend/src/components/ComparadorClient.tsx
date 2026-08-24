"use client";

import { useState } from "react";
import Link from "next/link";
import type { Parlamentar } from "@/lib/types";
import {
  calcularScore,
  faixaDoScore,
  percentualVotosCoerentes,
  resumoPromessas,
} from "@/lib/score";
import { formatarMoeda, rotuloCasa } from "@/lib/format";
import { totalGastos } from "@/data/mock";
import Avatar from "./Avatar";

interface ComparadorClientProps {
  parlamentares: Parlamentar[];
  inicialA?: string;
  inicialB?: string;
}

export default function ComparadorClient({
  parlamentares,
  inicialA,
  inicialB,
}: ComparadorClientProps) {
  const [idA, setIdA] = useState(inicialA ?? "");
  const [idB, setIdB] = useState(inicialB ?? "");

  const a = parlamentares.find((p) => p.id === idA);
  const b = parlamentares.find((p) => p.id === idB);

  function selecao(id: string, valor: string) {
    if (id === "a") setIdA(valor);
    else setIdB(valor);
  }

  return (
    <div>
      <div className="grid gap-4 sm:grid-cols-2">
        {(["a", "b"] as const).map((lado) => (
          <label key={lado} className="block rounded-xl border border-neutral-200 bg-white p-4 shadow-sm">
            <span className="mb-2 block text-sm font-semibold text-neutral-700">
              Parlamentar {lado.toUpperCase()}
            </span>
            <select
              value={lado === "a" ? idA : idB}
              onChange={(e) => selecao(lado, e.target.value)}
              className="min-h-11 w-full rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900"
            >
              <option value="">Selecione…</option>
              {parlamentares.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nome} ({p.partido}/{p.uf})
                </option>
              ))}
            </select>
          </label>
        ))}
      </div>

      {a && b && a.id !== b.id ? (
        <Comparacao a={a} b={b} />
      ) : (
        <p className="mt-8 rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
          {a && b && a.id === b.id
            ? "Selecione dois parlamentares diferentes para comparar."
            : "Selecione dois parlamentares acima para ver a comparação lado a lado."}
        </p>
      )}
    </div>
  );
}

function Comparacao({ a, b }: { a: Parlamentar; b: Parlamentar }) {
  const linhas = montarLinhas(a, b);

  return (
    <div className="mt-8 overflow-x-auto rounded-xl border border-slate-200 bg-white">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 bg-slate-50">
            <th className="px-4 py-3 text-left text-xs uppercase text-slate-500">Critério</th>
            {[a, b].map((p) => (
              <th key={p.id} className="px-4 py-3 text-left">
                <Link
                  href={`/parlamentares/${p.id}`}
                  className="flex items-center gap-3 hover:underline"
                >
                  <Avatar nome={p.nome} tamanho="sm" percentual={calcularScore(p.promessas, p.votacoes)} />
                  <span>
                    <span className="block font-semibold text-slate-900">{p.nome}</span>
                    <span className="text-xs font-normal text-slate-500">
                      {rotuloCasa(p.casa)} · {p.partido}/{p.uf}
                    </span>
                  </span>
                </Link>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {linhas.map((linha) => (
            <tr key={linha.rotulo}>
              <td className="px-4 py-3 font-medium text-slate-600">{linha.rotulo}</td>
              <td className="px-4 py-3 text-slate-900">{linha.valorA}</td>
              <td className="px-4 py-3 text-slate-900">{linha.valorB}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function montarLinhas(a: Parlamentar, b: Parlamentar) {
  const scoreA = calcularScore(a.promessas, a.votacoes);
  const scoreB = calcularScore(b.promessas, b.votacoes);
  const resumoA = resumoPromessas(a.promessas);
  const resumoB = resumoPromessas(b.promessas);
  const votosA = percentualVotosCoerentes(a.votacoes);
  const votosB = percentualVotosCoerentes(b.votacoes);

  const scoreComBarra = (score: number) => {
    const faixa = faixaDoScore(score);
    return (
      <span className="flex items-center gap-2">
        <span className={`text-lg font-bold ${faixa.texto}`}>{score}</span>
        <span className="h-2 w-24 overflow-hidden rounded-full bg-slate-200">
          <span className={`block h-full ${faixa.barra}`} style={{ width: `${score}%` }} />
        </span>
      </span>
    );
  };

  return [
    {
      rotulo: "Score de Coerência",
      valorA: scoreComBarra(scoreA),
      valorB: scoreComBarra(scoreB),
    },
    {
      rotulo: "Promessas cumpridas",
      valorA: `${resumoA.cumprida} de ${a.promessas.length}`,
      valorB: `${resumoB.cumprida} de ${b.promessas.length}`,
    },
    {
      rotulo: "Promessas em andamento",
      valorA: String(resumoA.em_andamento),
      valorB: String(resumoB.em_andamento),
    },
    {
      rotulo: "Promessas contraditadas",
      valorA: String(resumoA.contraditada),
      valorB: String(resumoB.contraditada),
    },
    {
      rotulo: "Proposições apresentadas",
      valorA: String(a.proposicoes.length),
      valorB: String(b.proposicoes.length),
    },
    {
      rotulo: "Votos coerentes com o discurso",
      valorA: `${votosA}% (${a.votacoes.filter((v) => v.coerenteComDiscurso).length}/${a.votacoes.length})`,
      valorB: `${votosB}% (${b.votacoes.filter((v) => v.coerenteComDiscurso).length}/${b.votacoes.length})`,
    },
    {
      rotulo: "Gasto total de gabinete (ano)",
      valorA: formatarMoeda(totalGastos(a)),
      valorB: formatarMoeda(totalGastos(b)),
    },
  ];
}
