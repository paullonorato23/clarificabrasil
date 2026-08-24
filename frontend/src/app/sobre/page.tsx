import type { Metadata } from "next";

export const metadata: Metadata = { title: "Sobre" };

export default function Sobre() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Projeto aberto</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Sobre a Política Transparente</h1>
      <p className="mt-4 text-lg leading-8 text-neutral-700">Uma plataforma colaborativa e sem fins lucrativos para acompanhar a atuação de deputados e senadores brasileiros com dados oficiais e critérios públicos.</p>
      <div className="mt-8 space-y-5 text-neutral-700">
        <section><h2 className="text-xl font-bold text-neutral-900">Independente e apartidária</h2><p className="mt-2">O projeto não aceita financiamento de partidos ou entidades com interesses legislativos.</p></section>
        <section><h2 className="text-xl font-bold text-neutral-900">Construída com fontes verificáveis</h2><p className="mt-2">Promessas passam por revisão da comunidade e devem apontar para a declaração original. Os dados de atividade parlamentar serão integrados às APIs oficiais da Câmara e do Senado.</p></section>
        <section className="rounded-xl border border-warning-200 bg-warning-50 p-5"><h2 className="font-bold text-warning-900">Versão de demonstração</h2><p className="mt-2 text-sm text-warning-900">Os dados atuais são fictícios e nenhuma informação é persistida. A integração com backend e fontes oficiais será implementada em uma etapa posterior.</p></section>
      </div>
    </div>
  );
}
