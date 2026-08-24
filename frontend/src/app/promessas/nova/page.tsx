import type { Metadata } from "next";
import { parlamentares } from "@/data/mock";
import FormularioPromessa from "@/components/FormularioPromessa";

export const metadata: Metadata = {
  title: "Cadastrar promessa",
  description: "Envie uma promessa de campanha com fonte verificável.",
};

function primeiroParametro(valor: string | string[] | undefined): string {
  return Array.isArray(valor) ? (valor[0] ?? "") : (valor ?? "");
}

export default async function NovaPromessa({ searchParams }: PageProps<"/promessas/nova">) {
  const parametros = await searchParams;
  const parlamentar = primeiroParametro(parametros.parlamentar);

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <p className="text-xs font-bold uppercase tracking-widest text-primary-700">Contribuição comunitária</p>
      <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-neutral-900">Cadastrar promessa</h1>
      <p className="mt-2 mb-8 text-neutral-600">Registre a citação original e uma fonte que qualquer pessoa possa conferir.</p>
      <FormularioPromessa
        parlamentares={parlamentares.map(({ id, nome }) => ({ id, nome }))}
        preselecionado={parlamentar}
      />
    </div>
  );
}
