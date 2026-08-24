"use client";

import { useState } from "react";

/**
 * Botões "Validar" / "Questionar" da fila de moderação.
 * Nesta fase sem backend, o voto é apenas registrado localmente (simulação).
 */
export default function BotoesValidacao() {
  const [voto, setVoto] = useState<"validar" | "questionar" | null>(null);

  if (voto) {
    return (
      <p className="text-sm font-medium text-emerald-700">
        ✓ {voto === "validar" ? "Validação" : "Questionamento"} registrado(a). Obrigado por
        participar! (simulação — nenhum dado foi salvo)
      </p>
    );
  }

  return (
    <div className="flex gap-2">
      <button
        onClick={() => setVoto("validar")}
        className="rounded-lg bg-emerald-700 px-3 py-1.5 text-xs font-semibold text-white hover:bg-emerald-800"
      >
        Validar
      </button>
      <button
        onClick={() => setVoto("questionar")}
        className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50"
      >
        Questionar
      </button>
    </div>
  );
}
