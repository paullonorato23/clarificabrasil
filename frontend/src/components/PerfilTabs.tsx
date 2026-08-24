"use client";

import { useState, type ReactNode } from "react";

export interface Aba {
  id: string;
  rotulo: string;
  conteudo: ReactNode;
}

/** Navegação por abas do perfil do parlamentar (conteúdo renderizado no servidor). */
export default function PerfilTabs({ abas }: { abas: Aba[] }) {
  const [ativa, setAtiva] = useState(abas[0]?.id);

  return (
    <div>
      <div role="tablist" aria-label="Seções do perfil" className="flex gap-1 overflow-x-auto border-b border-neutral-200">
        {abas.map((aba) => (
          <button
            key={aba.id}
            role="tab"
            aria-selected={ativa === aba.id}
            onClick={() => setAtiva(aba.id)}
            aria-controls={`painel-${aba.id}`}
            className={`rounded-t-lg border-b-2 px-4 py-2.5 text-sm font-medium whitespace-nowrap ${
              ativa === aba.id
                ? "border-primary-600 bg-primary-50 text-primary-800"
                : "border-transparent text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900"
            }`}
          >
            {aba.rotulo}
          </button>
        ))}
      </div>
      {abas.map((aba) => (
        <div
          key={aba.id}
          id={`painel-${aba.id}`}
          role="tabpanel"
          hidden={ativa !== aba.id}
          className={ativa === aba.id ? "block pt-6" : "hidden"}
        >
          {aba.conteudo}
        </div>
      ))}
    </div>
  );
}
