import type { Metadata } from "next";
import { PONTOS_POR_STATUS, PESO_PROMESSAS, PESO_VOTOS } from "@/lib/score";

export const metadata: Metadata = {
  title: "Metodologia",
  description: "Entenda como o Score de Coerência é calculado.",
};

export default function Metodologia() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Metodologia pública</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Como calculamos</h1>
      <p className="mt-3 text-lg leading-8 text-neutral-700">O Score de Coerência é uma leitura resumida, auditável e versionada da relação entre promessas registradas e comportamento em votações nominais.</p>
      <div className="mt-8 grid gap-5 sm:grid-cols-2">
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"><p className="font-data text-4xl font-extrabold text-primary-700">70%</p><h2 className="mt-2 text-xl font-bold text-neutral-900">Promessas</h2><p className="mt-1 text-sm text-neutral-600">A média dos status registrados tem maior peso no resultado.</p></section>
        <section className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"><p className="font-data text-4xl font-extrabold text-success-700">30%</p><h2 className="mt-2 text-xl font-bold text-neutral-900">Votações</h2><p className="mt-1 text-sm text-neutral-600">A proporção de votos coerentes completa o indicador.</p></section>
      </div>
      <section className="mt-8 rounded-xl border border-neutral-200 bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold text-neutral-900">Regras da versão 0.1</h2>
        <ul className="mt-4 space-y-3 text-neutral-700">
          <li><strong>{PONTOS_POR_STATUS.cumprida} ponto:</strong> promessa cumprida.</li>
          <li><strong>{PONTOS_POR_STATUS.em_andamento} ponto:</strong> promessa em andamento.</li>
          <li><strong>{PONTOS_POR_STATUS.sem_acao} ponto:</strong> sem ação identificada.</li>
          <li><strong>{PONTOS_POR_STATUS.contraditada} ponto:</strong> promessa contraditada.</li>
        </ul>
        <p className="mt-5 border-t border-neutral-200 pt-4 text-sm text-neutral-600">Fórmula: média das promessas × {PESO_PROMESSAS} + média das votações × {PESO_VOTOS}. Quando uma fonte não tem dados, a outra assume peso total.</p>
      </section>
    </div>
  );
}
