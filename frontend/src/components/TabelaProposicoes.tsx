"use client";

import { useMemo, useState } from "react";
import type { Proposicao, Tema, TipoProposicao } from "@/lib/types";
import { formatarData } from "@/lib/format";

const CORES_STATUS: Record<Proposicao["status"], string> = {
  "Em tramitação": "bg-sky-100 text-sky-800",
  Aprovada: "bg-emerald-100 text-emerald-800",
  Sancionada: "bg-emerald-100 text-emerald-800",
  Arquivada: "bg-slate-200 text-slate-600",
};

/** Tabela de proposições com filtro por tipo e tema (cliente). */
export default function TabelaProposicoes({ proposicoes }: { proposicoes: Proposicao[] }) {
  const [tipo, setTipo] = useState<TipoProposicao | "todos">("todos");
  const [tema, setTema] = useState<Tema | "todos">("todos");

  const temas = useMemo(
    () => [...new Set(proposicoes.map((p) => p.tema))].sort(),
    [proposicoes],
  );

  const filtradas = proposicoes.filter(
    (p) => (tipo === "todos" || p.tipo === tipo) && (tema === "todos" || p.tema === tema),
  );

  return (
    <div>
      <div className="mb-4 flex flex-wrap gap-3">
        <label className="text-sm text-slate-600">
          Tipo:{" "}
          <select
            value={tipo}
            onChange={(e) => setTipo(e.target.value as TipoProposicao | "todos")}
            className="min-h-11 rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900"
          >
            <option value="todos">Todos</option>
            <option value="PL">PL</option>
            <option value="PEC">PEC</option>
            <option value="REQ">Requerimento</option>
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Tema:{" "}
          <select
            value={tema}
            onChange={(e) => setTema(e.target.value as Tema | "todos")}
            className="min-h-11 rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900"
          >
            <option value="todos">Todos</option>
            {temas.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3">Proposição</th>
              <th className="px-4 py-3">Ementa</th>
              <th className="px-4 py-3">Tema</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Data</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filtradas.map((p) => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium whitespace-nowrap text-slate-900">
                  {p.tipo} {p.numero}
                </td>
                <td className="px-4 py-3 text-slate-700">{p.ementa}</td>
                <td className="px-4 py-3 whitespace-nowrap text-slate-600">{p.tema}</td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span
                    className={`rounded-full px-2.5 py-1 text-xs font-semibold ${CORES_STATUS[p.status]}`}
                  >
                    {p.status}
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-slate-600">
                  {formatarData(p.data)}
                </td>
              </tr>
            ))}
            {filtradas.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                  Nenhuma proposição encontrada com esses filtros.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
