"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import type { Tema } from "@/lib/types";

const TEMAS: Tema[] = [
  "Saúde",
  "Educação",
  "Meio Ambiente",
  "Economia",
  "Segurança",
  "Infraestrutura",
  "Direitos Humanos",
  "Transparência",
];

interface FormularioPromessaProps {
  parlamentares: { id: string; nome: string }[];
  preselecionado?: string;
}

/**
 * Formulário de cadastro colaborativo de promessa.
 * Nesta fase (sem backend), o envio é apenas simulado: exibe a confirmação
 * e orienta o usuário a acompanhar a fila de moderação.
 */
export default function FormularioPromessa({
  parlamentares,
  preselecionado,
}: FormularioPromessaProps) {
  const [enviada, setEnviada] = useState(false);

  function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setEnviada(true);
  }

  if (enviada) {
    return (
      <div className="rounded-xl border border-success-200 bg-success-50 p-6 text-center sm:p-8">
        <p className="text-4xl" aria-hidden>
          ✓
        </p>
        <h2 className="mt-2 text-xl font-bold text-success-900">
          Promessa enviada para moderação!
        </h2>
        <p className="mx-auto mt-2 max-w-md text-sm text-success-800">
          Obrigado por contribuir. A promessa ficará pendente até receber{" "}
          <strong>3 validações da comunidade</strong> ou a aprovação de um moderador.
          (Nesta versão de demonstração, nenhum dado foi realmente salvo.)
        </p>
        <div className="mt-6 flex flex-col justify-center gap-3 sm:flex-row">
          <Link
            href="/moderacao"
            className="inline-flex min-h-11 items-center justify-center rounded-lg bg-success-700 px-4 py-2 text-sm font-semibold text-white hover:bg-success-600"
          >
            Ver fila de moderação
          </Link>
          <button
            onClick={() => setEnviada(false)}
            className="min-h-11 rounded-lg border border-success-300 bg-white px-4 py-2 text-sm font-semibold text-success-800 hover:bg-success-100"
          >
            Cadastrar outra
          </button>
        </div>
      </div>
    );
  }

  const campo =
    "mt-1 min-h-11 w-full rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 focus:border-primary-500 focus:outline-none";

  return (
    <form
      onSubmit={aoEnviar}
      className="space-y-5 rounded-xl border border-neutral-200 bg-white p-5 shadow-sm sm:p-6"
    >
      <div>
        <label htmlFor="parlamentar" className="text-sm font-semibold text-neutral-700">
          Parlamentar *
        </label>
        <select
          id="parlamentar"
          name="parlamentar"
          required
          defaultValue={preselecionado ?? ""}
          className={campo}
        >
          <option value="" disabled>
            Selecione…
          </option>
          {parlamentares.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nome}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="texto" className="text-sm font-semibold text-neutral-700">
          Texto exato da promessa *
        </label>
        <textarea
          id="texto"
          name="texto"
          required
          rows={3}
          placeholder="Transcreva a promessa exatamente como foi dita ou escrita (citação direta)."
          className={campo}
        />
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="fonteUrl" className="text-sm font-semibold text-neutral-700">
            Link da fonte *
          </label>
          <input
            id="fonteUrl"
            name="fonteUrl"
            type="url"
            required
            placeholder="https://…"
            className={campo}
          />
          <p className="mt-1 text-xs text-neutral-500">
            Site oficial, vídeo de debate (com timestamp), post oficial, entrevista ou
            panfleto digitalizado.
          </p>
        </div>
        <div>
          <label htmlFor="fonteDescricao" className="text-sm font-semibold text-neutral-700">
            Descrição da fonte *
          </label>
          <input
            id="fonteDescricao"
            name="fonteDescricao"
            required
            placeholder="Ex.: Entrevista ao Jornal X — 12/09/2022"
            className={campo}
          />
        </div>
      </div>

      <div className="grid gap-5 sm:grid-cols-3">
        <div>
          <label htmlFor="data" className="text-sm font-semibold text-neutral-700">
            Data da declaração *
          </label>
          <input id="data" name="data" type="date" required className={campo} />
        </div>
        <div>
          <label htmlFor="tema" className="text-sm font-semibold text-neutral-700">
            Categoria temática *
          </label>
          <select id="tema" name="tema" required defaultValue="" className={campo}>
            <option value="" disabled>
              Selecione…
            </option>
            {TEMAS.map((tema) => (
              <option key={tema} value={tema}>
                {tema}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="eleicao" className="text-sm font-semibold text-neutral-700">
            Eleição de referência *
          </label>
          <select id="eleicao" name="eleicao" required defaultValue="2022" className={campo}>
            <option value="2022">2022</option>
            <option value="2018">2018</option>
          </select>
        </div>
      </div>

      <div className="rounded-lg bg-neutral-100 p-4 text-sm text-neutral-700">
        <p className="font-semibold text-neutral-800">Não serão aceitas:</p>
        <ul className="mt-1 list-inside list-disc space-y-0.5">
          <li>promessas sem fonte verificável;</li>
          <li>interpretações ou paráfrases sem a citação original;</li>
          <li>conteúdo de humor, sátira ou meme;</li>
          <li>informações envolvendo menores de idade.</li>
        </ul>
      </div>

      <button
        type="submit"
        className="min-h-12 w-full rounded-lg bg-primary-700 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-600 active:bg-primary-800"
      >
        Enviar para moderação
      </button>
    </form>
  );
}
